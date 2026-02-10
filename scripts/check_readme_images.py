#!/usr/bin/env python3
"""Simple README image/asset URL checker.
Scans README.md for image links and checks their HTTP status or file existence.
"""
import re
import sys
import os
from urllib.parse import urlparse

try:
    import requests
except Exception:
    requests = None

ROOT = os.path.dirname(os.path.dirname(__file__))
README = os.path.join(ROOT, 'README.md')
TIMEOUT = 10

IMG_REGEX = re.compile(r"(?:<img\s+[^>]*src=\"([^\"]+)\"|!\[[^\]]*\]\(([^)]+)\))", re.IGNORECASE)


def check_url(url):
    parsed = urlparse(url)
    if parsed.scheme in ('http', 'https'):
        if requests:
            try:
                r = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
                return r.status_code, r.url
            except Exception:
                try:
                    r = requests.get(url, allow_redirects=True, timeout=TIMEOUT)
                    return r.status_code, r.url
                except Exception as e:
                    return f'ERR: {e}', url
        else:
            # fallback to urllib
            import urllib.request
            req = urllib.request.Request(url, method='HEAD')
            try:
                with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
                    return res.getcode(), res.geturl()
            except Exception as e:
                return f'ERR: {e}', url
    else:
        # treat as local path
        path = os.path.join(ROOT, url)
        exists = os.path.exists(path)
        return ('LOCAL_OK' if exists else 'LOCAL_MISSING'), os.path.abspath(path)


def main():
    if not os.path.exists(README):
        print('README.md not found at', README)
        sys.exit(2)

    text = open(README, 'r', encoding='utf-8').read()
    found = []
    for m in IMG_REGEX.finditer(text):
        url = m.group(1) or m.group(2)
        url = url.strip()
        if not url:
            continue
        # remove optional title after URL in markdown: ![alt](url "title")
        if url.startswith('http') or url.startswith('/') or url.startswith('./') or url.startswith('../') or url.startswith('data:'):
            found.append(url)
        else:
            found.append(url)

    if not found:
        print('No image links found in README.md')
        return

    print(f'Found {len(found)} image/link(s). Checking...')
    problems = []
    for url in found:
        status, final = check_url(url)
        ok = False
        if isinstance(status, int):
            ok = 200 <= status < 400
        elif status in ('LOCAL_OK',):
            ok = True
        if ok:
            print(f'OK  {status}  {url} -> {final}')
        else:
            print(f'BAD {status}  {url} -> {final}')
            problems.append((url, status, final))

    print('\nSummary:')
    if not problems:
        print('All image links look reachable.')
    else:
        print(f'{len(problems)} problematic link(s):')
        for url, status, final in problems:
            print('-', url, 'status=', status, 'final=', final)


if __name__ == '__main__':
    main()

import urllib.request, re, json, gzip

url = 'https://loja.marykay.com.br/todos-os-produtos'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'})
resp = urllib.request.urlopen(req, timeout=15)
data = gzip.decompress(resp.read())
html = data.decode('utf-8')

# Look for __RUNTIME__ or __STATE__ or similar
patterns = [
    r'__RUNTIME__\s*=\s*({[^<]+})',
    r'__STATE__\s*=\s*({[^<]+})',
    r'__INITIAL_STATE__\s*=\s*({[^<]+})',
    r'__NEXT_DATA__\s*=\s*({[^<]+})',
    r'window\.__([A-Z_]+)\s*=',
    r'vtex\.render\.render',
    r'\"api\"',
    r'/api/catalog',
]
for p in patterns:
    matches = re.findall(p, html)
    if matches:
        print(f'{p}: {len(matches)} matches')
        for m in matches[:3]:
            print(f'  {m[:300]}')
        print()

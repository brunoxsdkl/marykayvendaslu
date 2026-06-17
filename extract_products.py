import urllib.request, re, json, gzip, os

url = 'https://loja.marykay.com.br/todos-os-produtos?page=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'})
resp = urllib.request.urlopen(req, timeout=15)
data = gzip.decompress(resp.read())
html = data.decode('utf-8')

# Find img URLs for products
imgs = re.findall(r'https://[^"\']+?(?:jpg|jpeg|png|webp)[^"\']*', html)
print(f'Found {len(imgs)} images')
for img in imgs[:50]:
    print(img)

print("\n\n=== Product names ===")
# Find product names
names = re.findall(r'<h3[^>]*>([^<]+)</h3>', html)
print(f'Found {len(names)} product names')
for n in names:
    print(n)

print("\n\n=== Prices ===")
# Find prices
prices = re.findall(r'R\$\s*[\d.,]+', html)
for p in prices[:30]:
    print(p)

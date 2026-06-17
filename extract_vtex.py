import urllib.request, json, gzip, re

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip'
    })
    resp = urllib.request.urlopen(req, timeout=30)
    data = gzip.decompress(resp.read())
    return json.loads(data.decode())

# VTEX Search API
base = "https://loja.marykay.com.br/api/catalog_system/pub/products/search"
url = f"{base}?_from=0&_to=50"
try:
    products = fetch_json(url)
    print(f"Total products: {len(products)}")
    for p in products[:5]:
        name = p.get('productName', 'N/A')
        pid = p.get('productId', 'N/A')
        price = p.get('priceRange', {}).get('sellingPrice', {}).get('highPrice', 0)
        imgs = p.get('items', [{}])[0].get('images', [])
        img_url = imgs[0].get('imageUrl', '') if imgs else ''
        print(f"\n--- {name} ---")
        print(f"ID: {pid}")
        print(f"Price: {price}")
        print(f"Image: {img_url}")
except Exception as e:
    print(f"Error: {e}")

# Try alternative: VTEX search with specific department
print("\n\n=== Trying different URLs ===")
for path in [
    "/api/catalog_system/pub/products/search",
    "/api/catalog_system/pvt/products/GetProductAndSkuIds",
]:
    url = f"https://loja.marykay.com.br{path}"
    print(f"\nTrying: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=15)
        print(f"Status: {resp.status}")
        print(resp.read()[:500])
    except Exception as e:
        print(f"Error: {e}")

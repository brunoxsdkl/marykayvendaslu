import urllib.request, json, gzip, os, re

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip'
    })
    resp = urllib.request.urlopen(req, timeout=30)
    data = gzip.decompress(resp.read())
    return json.loads(data.decode())

base = "https://loja.marykay.com.br/api/catalog_system/pub/products/search"
all_products = []
page = 0
page_size = 50

while True:
    frm = page * page_size
    to = frm + page_size - 1
    url = f"{base}?_from={frm}&_to={to}"
    print(f"Fetching page {page+1} (items {frm}-{to})...")
    try:
        products = fetch_json(url)
        if not products:
            break
        all_products.extend(products)
        page += 1
        if len(products) < page_size:
            break
    except Exception as e:
        print(f"Error: {e}")
        break

print(f"\nTotal products fetched: {len(all_products)}")

# Extract useful fields
output = []
for p in all_products:
    name = p.get('productName', '')
    pid = p.get('productId', '')
    link = p.get('linkText', '')
    category = p.get('categoryId', '')
    categories = p.get('categories', [])
    # Get price
    price = 0
    items = p.get('items', [])
    if items:
        sellers = items[0].get('sellers', [])
        if sellers:
            comm = sellers[0].get('commertialOffer', {})
            price = comm.get('Price', 0)
        images = items[0].get('images', [])
        img_url = images[0].get('imageUrl', '') if images else ''
    else:
        img_url = ''
    
    # Get category name
    cat_name = ''
    if categories:
        parts = [c.strip('/') for c in categories[0].split('/') if c.strip('/')]
        cat_name = parts[-1] if parts else ''
    
    product = {
        'id': pid,
        'name': name,
        'price': price,
        'image': img_url,
        'link': link,
        'category': cat_name,
        'categories': [c.strip('/') for c in categories[0].split('/') if c.strip('/')] if categories else []
    }
    output.append(product)
    print(f"  {name} - R$ {price:.2f} - {cat_name}")

# Save to JSON
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\nSaved to products.json")

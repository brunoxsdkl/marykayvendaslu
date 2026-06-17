import urllib.request, json, gzip, os, sys

sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)

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

print(f"Total products fetched: {len(all_products)}")

output = []
for p in all_products:
    name = p.get('productName', '')
    pid = p.get('productId', '')
    link = p.get('linkText', '')
    categories = p.get('categories', [])
    price = 0
    items = p.get('items', [])
    img_url = ''
    if items:
        sellers = items[0].get('sellers', [])
        if sellers:
            comm = sellers[0].get('commertialOffer', {})
            price = comm.get('Price', 0) / 100
        images = items[0].get('images', [])
        if images:
            img_url = images[0].get('imageUrl', '').replace('http://', 'https://')
    
    cat_name = ''
    cat_hierarchy = []
    if categories:
        parts = [c.strip('/') for c in categories[0].split('/') if c.strip('/')]
        cat_hierarchy = parts
        cat_name = parts[-1] if parts else ''
    
    description = p.get('description', '')
    brand = p.get('brand', '')
    
    product = {
        'id': pid,
        'name': name,
        'price': price,
        'image': img_url,
        'link': link,
        'category': cat_name,
        'category_path': '/'.join(cat_hierarchy),
        'brand': brand,
        'description': description[:200] if description else ''
    }
    output.append(product)

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"Saved {len(output)} products to products.json")

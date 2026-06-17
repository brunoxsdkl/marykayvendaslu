import json

with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for p in products:
    # Price is already in reais, fix it (was divided by 100 incorrectly)
    p['price'] = round(p['price'] * 100, 2)

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"Fixed prices for {len(products)} products")
# Show first few
for p in products[:5]:
    print(f"{p['name']}: R$ {p['price']}")

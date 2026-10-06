import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storefront.settings")
django.setup()

from store.models import Collection, Product

# Clear existing data (optional)
Product.objects.all().delete()
Collection.objects.all().delete()

# Collections
electronics = Collection.objects.create(title="Electronics")
accessories = Collection.objects.create(title="Accessories")
clothing = Collection.objects.create(title="Clothing")
footwear = Collection.objects.create(title="Footwear")
bags = Collection.objects.create(title="Bags")

# Products
products = [
    ("Wireless Headphones", "Noise cancelling wireless headphones", 8500, 25, electronics),
    ("Mechanical Keyboard", "RGB mechanical keyboard", 6500, 15, electronics),
    ("USB-C Cable", "Fast charging USB-C cable", 1200, 100, accessories),
    ("Laptop Stand", "Adjustable aluminium laptop stand", 4500, 30, accessories),
    ("Running Shoes", "Comfortable running shoes", 7500, 20, footwear),
    ("Cotton T-Shirt", "Comfortable cotton t-shirt", 1800, 50, clothing),
    ("Smart Watch", "Fitness tracking smart watch", 12000, 10, electronics),
    ("Travel Backpack", "Water-resistant travel backpack", 3500, 40, bags),
]

for title, description, price, inventory, collection in products:
    Product.objects.create(
        title=title,
        description=description,
        unit_price=price,
        inventory=inventory,
        collection=collection
    )

print("Dataset loaded successfully!")
import time
from faker import Faker
from faker_commerce import Provider
import random
import json

fake = Faker()
fake.add_provider(Provider)

def product_generator(n):
    base_id = 100_000

    for i in range(n):
        yield {
            "id": base_id + i,
            "product_name": fake.ecommerce_name() if hasattr(fake, 'ecommerce_name') else fake.catch_phrase(),
            "price": round(random.uniform(5.00, 499.99), 2),
            "category": fake.ecommerce_category() if hasattr(fake, 'ecommerce_category') else fake.bs()
        }

def pretty_print(catalog):
    print(json.dumps(catalog, indent=2))
    
def linear_search(product_id, products):
  for product in products:
    if product_id == product["id"]:
      return product
    
def filter_product(product,search_id):
   return products['id'] == search_id

def linear_search_filter(product_id, products):
  return list(filter(lambda product: filter_product(product, product_id), products))

def binary_search(product_id, products):
   first_part = 0
   last_part = len(products) - 1

   while first_part <= last_part:
        middle = (first + last) // 2
        if products[middle]['id'] == product_id:
             return products[middle]
        elif products[middle]['id'] < product_id:
             first_part = middle + 1
        else:
             last_part = middle - 1

def hash_search(product_id, products):
    product_dict = {product['id']: product for product in products}
    return product_dict.get(product_id, None)
   

if __name__ == "__main__":
    N = 1_000
    print(f"Generating {N:,} products...")
    
    products = list(product_generator(N))
    
    # print("sample product: ")
    # print(pretty_print(products[0]))
    
    sample_product_id = 100_065
    
    # product = linear_search(sample_product_id, products)
    # print(product)
    
    product = hash_search(sample_product_id, products)
    print(f"Hash search Product found: {product}")

    
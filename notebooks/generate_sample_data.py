# notebooks/generate_sample_data.py

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# --- Configuration ---
NUM_CUSTOMERS = 200
NUM_PRODUCTS = 50
NUM_ORDERS = 500
NUM_ORDER_ITEMS = 1000
NUM_PAYMENTS = 600

# Initialize Faker for generating mock data
fake = Faker()

# --- Define Output Directory ---
# The script is in /notebooks, so we need to go one level up ('../') to find the /data directory.
output_dir = '../data/raw'
# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# --- 1. Generate Customers ---
print("Generating customers...")
customers_data = []
for _ in range(NUM_CUSTOMERS):
    customers_data.append({
        'customer_id': fake.uuid4(),
        'customer_name': fake.name(),
        'email': fake.email(),
        'address': fake.address().replace('\n', ', '),
        'signup_date': fake.date_time_this_decade().date()
    })
customers_df = pd.DataFrame(customers_data)
print(f"Generated {len(customers_df)} customers.")

# --- 2. Generate Products ---
print("\nGenerating products...")
products_data = []
product_categories = ['Electronics', 'Books', 'Clothing', 'Home Goods', 'Sports', 'Toys']
for _ in range(NUM_PRODUCTS):
    products_data.append({
        'product_id': fake.uuid4(),
        'product_name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
        'category': random.choice(product_categories),
        'price': round(random.uniform(5.0, 500.0), 2)
    })
products_df = pd.DataFrame(products_data)
print(f"Generated {len(products_df)} products.")

# --- 3. Generate Orders ---
print("\nGenerating orders...")
orders_data = []
customer_ids = customers_df['customer_id'].tolist()
for _ in range(NUM_ORDERS):
    order_date = fake.date_time_between(start_date='-2y', end_date='now')
    orders_data.append({
        'order_id': fake.uuid4(),
        'customer_id': random.choice(customer_ids),
        'order_date': order_date.date(),
        'status': random.choice(['pending', 'shipped', 'delivered', 'cancelled'])
    })
orders_df = pd.DataFrame(orders_data)
print(f"Generated {len(orders_df)} orders.")

# --- 4. Generate Order Items ---
print("\nGenerating order items...")
order_items_data = []
order_ids = orders_df['order_id'].tolist()
product_ids = products_df['product_id'].tolist()
for _ in range(NUM_ORDER_ITEMS):
    order_items_data.append({
        'order_item_id': fake.uuid4(),
        'order_id': random.choice(order_ids),
        'product_id': random.choice(product_ids),
        'quantity': random.randint(1, 5)
    })
order_items_df = pd.DataFrame(order_items_data)
print(f"Generated {len(order_items_df)} order items.")

# --- 5. Generate Payments ---
print("\nGenerating payments...")
payments_data = []
# We only want payments for orders that were not cancelled
order_ids_for_payment = orders_df[orders_df['status'] != 'cancelled']['order_id'].tolist()

# Create a mapping of product_id to price for quick lookup
price_map = products_df.set_index('product_id')['price'].to_dict()
# Create a mapping of order_id to its items
order_items_map = order_items_df.groupby('order_id')['product_id'].apply(list)
order_quantity_map = order_items_df.groupby(['order_id', 'product_id'])['quantity'].sum().to_dict()

for order_id in random.sample(order_ids_for_payment, min(len(order_ids_for_payment), NUM_PAYMENTS)):
    order_date = orders_df.loc[orders_df['order_id'] == order_id, 'order_date'].iloc[0]

    # Calculate the total amount for the order
    amount = 0
    if order_id in order_items_map:
        for product_id in order_items_map[order_id]:
            quantity = order_quantity_map.get((order_id, product_id), 0)
            price = price_map.get(product_id, 0)
            amount += quantity * price

    if amount > 0:
        payments_data.append({
            'payment_id': fake.uuid4(),
            'order_id': order_id,
            'payment_date': order_date + timedelta(days=random.randint(0, 3)),
            'amount': round(amount, 2),
            'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer'])
        })
payments_df = pd.DataFrame(payments_data)
print(f"Generated {len(payments_df)} payments.")

# --- Save to CSV ---
print(f"\nSaving files to {output_dir}...")
customers_df.to_csv(f"{output_dir}/customers.csv", index=False)
products_df.to_csv(f"{output_dir}/products.csv", index=False)
orders_df.to_csv(f"{output_dir}/orders.csv", index=False)
order_items_df.to_csv(f"{output_dir}/order_items.csv", index=False)
payments_df.to_csv(f"{output_dir}/payments.csv", index=False)

print("\nSample data generation complete!")
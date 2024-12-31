import os
import pandas as pd
from faker import Faker
from confluent_kafka import Producer
from dotenv import load_dotenv
import json

load_dotenv()

fake = Faker("pt-BR")

regions = ["Sul", "Sudeste", "Centro-Oeste", "Norte", "Nordeste"]

vendors = ["Vendedor 1", "Vemdedor 2", "Vendedor 3", "Vendedor 4", "Vendedor 5"]

products = [
    ("Joranda de Dados", 2000),
    ("Bootcamp Python", 500),
    ("Bootcamp SQL", 500),
    ("Bootcamp Cloud", 1000),
]

def generate_fake_orders(start_date="today", end_date="today"):
    quantity = fake.random_int(min=1, max=10)
    product = fake.random_element(elements=products)
    product_name = product[0]
    total_price = product[1] * quantity

    return {
        "order_id": fake.uuid4(),
        "order_date": str(fake.date_between(start_date=start_date, end_date=end_date)),
        "region": fake.random_element(elements=regions),
        "vendor": fake.random_element(elements=vendors),
        "product_name": product_name,
        "quantity": quantity,
        "total_price": total_price,
    }

def generate_fake_orders_parquet(n_rows=10000):
    # Resolve the absolute path for the data directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")

    # Ensure the 'data' directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Full path for the output file
    output_file = os.path.join(data_dir, "orders.parquet")

    # Generate data and save to the file
    data = [generate_fake_orders(start_date="-30d",end_date="-1d") for _ in range(n_rows)]
    pd.DataFrame(data).to_parquet(output_file, index=False)

producer_conf = {
    # Required connection configs for Kafka producer, consumer, and admin
    "bootstrap.servers": os.environ["BOOTSTRAP_SERVERS"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.environ["SASL_USERNAME"],
    "sasl.password": os.environ["SASL_PASSWORD"],
}

producer = Producer(producer_conf)

def generate_message(data):
    key = data["order_id"]
    value = json.dumps(data).encode("utf-8")
    producer.produce(topic="orders", key=key, value=value)
    print(f"Order {key} sent")
    producer.flush()

if __name__ == "__main__":
    while True:
        data = generate_fake_orders()
        generate_message(data)
    


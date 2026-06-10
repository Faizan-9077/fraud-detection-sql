from faker import Faker
import pandas as pd
import numpy as np
import random
import uuid
import os


fake = Faker("en_IN")

Faker.seed(42)
random.seed(42)
np.random.seed(42)


OUTPUT_DIR = "generated_data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "customers.csv")

NUM_CUSTOMERS = 10000

CUSTOMER_COLUMNS = [
    "customer_id",
    "full_name",
    "gender",
    "date_of_birth",
    "phone_number",
    "email",
    "address",
    "city",
    "state",
    "occupation",
    "annual_income",
    "kyc_status",
    "customer_since",
    "risk_profile"
]

OCCUPATIONS = [
    "Student",
    "Engineer",
    "Doctor",
    "Teacher",
    "Business",
    "Government Employee",
    "Private Employee",
    "Farmer",
    "Self Employed",
    "Retired"
]

KYC_STATUS = [
    "Completed",
    "Pending"
]

RISK_PROFILES = [
    "Low",
    "Medium",
    "High"
]

GENDERS = [
    "Male",
    "Female"
]

def generate_customer():
    gender = random.choice(GENDERS)

    customer = {
        "customer_id": str(uuid.uuid4()),
        "full_name": fake.name(),
        "gender": gender,
        "date_of_birth": fake.date_of_birth(
            minimum_age=18,
            maximum_age=80
        ),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "address": fake.address().replace("\n", ", "),
        "city": fake.city(),
        "state": fake.state(),
        "occupation": random.choice(OCCUPATIONS),
        "annual_income": random.randint(200000, 2000000),
        "kyc_status": random.choices(
            KYC_STATUS,
            weights=[80, 20]
        )[0],
        "customer_since": fake.date_between(
            start_date="-10y",
            end_date="today"
        ),
        "risk_profile": random.choices(
            RISK_PROFILES,
            weights=[70, 20, 10]
        )[0]
    }

    return customer

def generate_customer_data():
    customers = []

    for _ in range(NUM_CUSTOMERS):
        customers.append(generate_customer())

    return pd.DataFrame(customers)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = generate_customer_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(df.head())
    print("\nTotal customers generated:", len(df))
    print(f"\nCustomer data saved to: {OUTPUT_FILE}")

    print("\nKYC Status Distribution:")
    print(df["kyc_status"].value_counts())

    print("\nRisk Profile Distribution:")
    print(df["risk_profile"].value_counts())
from faker import Faker
import pandas as pd
import numpy as np
import random
import os
import string

# ---------------------------------
# Setup
# ---------------------------------

fake = Faker("en_IN")

SEED = 42

Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = "generated_data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "customers.csv")

NUM_CUSTOMERS = 50000

RISK_RATINGS = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

# ---------------------------------
# Unique Value Trackers
# ---------------------------------

used_cif = set()
used_pan = set()
used_aadhar = set()
used_phone = set()

# ---------------------------------
# Helper Functions
# ---------------------------------

def generate_cif():

    while True:
        cif = "CIF" + ''.join(random.choices(string.digits, k=10))

        if cif not in used_cif:
            used_cif.add(cif)
            return cif


def generate_pan():

    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=5))
        digits = ''.join(random.choices(string.digits, k=4))
        last_letter = random.choice(string.ascii_uppercase)

        pan = letters + digits + last_letter

        if pan not in used_pan:
            used_pan.add(pan)
            return pan


def generate_aadhar():

    while True:
        aadhar = ''.join(random.choices(string.digits, k=12))

        if aadhar not in used_aadhar:
            used_aadhar.add(aadhar)
            return aadhar


def generate_phone_number():

    while True:
        first_digit = random.choice(["6", "7", "8", "9"])
        remaining_digits = ''.join(random.choices(string.digits, k=9))

        phone = first_digit + remaining_digits

        if phone not in used_phone:
            used_phone.add(phone)
            return phone


# ---------------------------------
# Customer Generator
# ---------------------------------

def generate_customer():

    customer = {
        "customer_id": generate_cif(),
        "first_name": fake.first_name(),
        "middle_name": fake.first_name(),
        "last_name": fake.last_name(),
        "dob": fake.date_of_birth(
            minimum_age=18,
            maximum_age=80
        ),
        "pan_number": generate_pan(),
        "aadhar": generate_aadhar(),
        "phone_number": generate_phone_number(),
        "email": fake.unique.email(),
        "risk_rating": random.choices(
            RISK_RATINGS,
            weights=[70, 20, 10]
        )[0],
        "created_at": fake.date_time_between(
            start_date="-10y",
            end_date="now"
        )
    }

    return customer


# ---------------------------------
# Generate Customer Dataset
# ---------------------------------

def generate_customer_data():

    fake.unique.clear()

    customers = []

    for _ in range(NUM_CUSTOMERS):
        customers.append(
            generate_customer()
        )

    return pd.DataFrame(customers)


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = generate_customer_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(df.head())

    print("\nTotal Customers Generated:")
    print(len(df))

    print("\nRisk Rating Distribution:")
    print(df["risk_rating"].value_counts())

    print(f"\nCustomer data saved to: {OUTPUT_FILE}")

    # ---------------------------------
    # Data Validation
    # ---------------------------------

    print("\nDuplicate CIF Numbers:")
    print(df["customer_id"].duplicated().sum())

    print("\nDuplicate PAN Numbers:")
    print(df["pan_number"].duplicated().sum())

    print("\nDuplicate Aadhaar Numbers:")
    print(df["aadhar"].duplicated().sum())

    print("\nDuplicate Phone Numbers:")
    print(df["phone_number"].duplicated().sum())

    print("\nDuplicate Email Addresses:")
    print(df["email"].duplicated().sum())
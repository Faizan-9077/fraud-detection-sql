from faker import Faker
import pandas as pd
import numpy as np
import random
import os

# ---------------------------------
# Setup
# ---------------------------------

fake = Faker("en_IN")

SEED = 42

Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

INPUT_FILE = "generated_data/customers.csv"

OUTPUT_DIR = "generated_data"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "kyc_records.csv"
)

KYC_STATUS = [
    "COMPLETED",
    "PENDING",
    "REJECTED"
]

# ---------------------------------
# Generate KYC Dataset
# ---------------------------------

def generate_kyc_data():

    customers_df = pd.read_csv(INPUT_FILE)

    kyc_records = []

    for index, row in customers_df.iterrows():

        kyc = {
            "kyc_id": index + 1,
            "customer_id": row["customer_id"],
            "status": random.choices(
                KYC_STATUS,
                weights=[80, 15, 5]
            )[0],
            "review_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            )
        }

        kyc_records.append(kyc)

    return pd.DataFrame(kyc_records)


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = generate_kyc_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(df.head())

    print("\nTotal KYC Records Generated:")
    print(len(df))

    print(f"\nKYC data saved to: {OUTPUT_FILE}")

    print("\nKYC Status Distribution:")
    print(df["status"].value_counts())

    # ---------------------------------
    # Data Validation
    # ---------------------------------

    print("\nDuplicate KYC IDs:")
    print(df["kyc_id"].duplicated().sum())

    print("\nDuplicate Customer IDs:")
    print(df["customer_id"].duplicated().sum())
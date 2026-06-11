import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# --------------------------------------------------
# Deterministic Seed
# --------------------------------------------------

random.seed(42)
np.random.seed(42)

fake = Faker("en_IN")
Faker.seed(42)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

accounts_df = pd.read_csv("generated_data/accounts.csv")
fatf_df = pd.read_csv("generated_data/fatf_high_risk_countries.csv")

account_ids = accounts_df["account_id"].tolist()
country_ids = fatf_df["country_id"].tolist()

# --------------------------------------------------
# Exact Beneficiary Distribution
# 30% -> 1
# 40% -> 2
# 20% -> 3
# 10% -> 4
# --------------------------------------------------

shuffled_accounts = account_ids.copy()
random.shuffle(shuffled_accounts)

one_beneficiary = shuffled_accounts[:19500]
two_beneficiary = shuffled_accounts[19500:45500]
three_beneficiary = shuffled_accounts[45500:58500]
four_beneficiary = shuffled_accounts[58500:]

# --------------------------------------------------
# Generate Beneficiaries
# --------------------------------------------------

beneficiaries = []

beneficiary_counter = 1
beneficiary_account_number = 200000000001

today = datetime.today()

def create_beneficiary(account_id):

    global beneficiary_counter
    global beneficiary_account_number

    beneficiary = {
        "beneficiary_id": f"BEN{beneficiary_counter:08d}",
        "account_id": account_id,
        "beneficiary_name": fake.name(),
        "beneficiary_account_number": beneficiary_account_number,
        "country_id": random.choice(country_ids),
        "created_at": (
            today - timedelta(
                days=random.randint(1, 730)
            )
        ).strftime("%Y-%m-%d")
    }

    beneficiary_counter += 1
    beneficiary_account_number += 1

    return beneficiary

# --------------------------------------------------
# One Beneficiary Accounts
# --------------------------------------------------

for account_id in one_beneficiary:
    beneficiaries.append(
        create_beneficiary(account_id)
    )

# --------------------------------------------------
# Two Beneficiary Accounts
# --------------------------------------------------

for account_id in two_beneficiary:
    for _ in range(2):
        beneficiaries.append(
            create_beneficiary(account_id)
        )

# --------------------------------------------------
# Three Beneficiary Accounts
# --------------------------------------------------

for account_id in three_beneficiary:
    for _ in range(3):
        beneficiaries.append(
            create_beneficiary(account_id)
        )

# --------------------------------------------------
# Four Beneficiary Accounts
# --------------------------------------------------

for account_id in four_beneficiary:
    for _ in range(4):
        beneficiaries.append(
            create_beneficiary(account_id)
        )

# --------------------------------------------------
# Create DataFrame
# --------------------------------------------------

beneficiary_df = pd.DataFrame(beneficiaries)

# --------------------------------------------------
# Validation
# --------------------------------------------------

assert len(beneficiary_df) == 136500

assert beneficiary_df[
    "beneficiary_id"
].is_unique

assert beneficiary_df[
    "beneficiary_account_number"
].is_unique

assert beneficiary_df[
    "account_id"
].notnull().all()

assert beneficiary_df[
    "country_id"
].notnull().all()

beneficiary_counts = (
    beneficiary_df
    .groupby("account_id")
    .size()
)

assert (beneficiary_counts == 1).sum() == 19500
assert (beneficiary_counts == 2).sum() == 26000
assert (beneficiary_counts == 3).sum() == 13000
assert (beneficiary_counts == 4).sum() == 6500

# --------------------------------------------------
# Save CSV
# --------------------------------------------------

output_path = "generated_data/beneficiaries.csv"

beneficiary_df.to_csv(
    output_path,
    index=False
)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("=" * 60)
print("Beneficiaries Generation Completed")
print("=" * 60)

print(
    f"Total Beneficiaries Generated : "
    f"{len(beneficiary_df)}"
)

print()

print("Account -> Beneficiary Distribution")
print(
    beneficiary_counts
    .value_counts()
    .sort_index()
)

print()

print(
    f"CSV Saved Successfully : "
    f"{output_path}"
)

print("=" * 60)
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# -----------------------------------
# Deterministic Seed
# -----------------------------------

random.seed(42)
np.random.seed(42)

# -----------------------------------
# Load Data
# -----------------------------------

customers_df = pd.read_csv("generated_data/customers.csv")
branches_df = pd.read_csv("generated_data/branches.csv")

customer_ids = customers_df["customer_id"].tolist()
branch_ids = branches_df["branch_id"].tolist()

# -----------------------------------
# Create Exact Account Distribution
# -----------------------------------

shuffled_customers = customer_ids.copy()
random.shuffle(shuffled_customers)

one_account_customers = shuffled_customers[:37500]
two_account_customers = shuffled_customers[37500:47500]
three_account_customers = shuffled_customers[47500:]

accounts = []

account_number = 100000000001
today = datetime.today()

# -----------------------------------
# Helper Function
# -----------------------------------

def create_account(customer_id, account_number):

    account_type = np.random.choice(
        ["SAVINGS", "CURRENT"],
        p=[0.80, 0.20]
    )

    if account_type == "SAVINGS":
        balance = round(random.uniform(1000, 1000000), 2)
    else:
        balance = round(random.uniform(10000, 5000000), 2)

    status = np.random.choice(
        ["ACTIVE", "DORMANT", "CLOSED"],
        p=[0.85, 0.10, 0.05]
    )

    if status == "ACTIVE":
        days = random.randint(1, 90)
    elif status == "DORMANT":
        days = random.randint(91, 365)
    else:
        days = random.randint(180, 365)

    last_active_date = (
        today - timedelta(days=days)
    ).strftime("%Y-%m-%d")

    return {
        "account_id": account_number,
        "customer_id": customer_id,
        "branch_id": random.choice(branch_ids),
        "account_type": account_type,
        "balance": balance,
        "status": status,
        "last_active_date": last_active_date,
    }

# -----------------------------------
# Generate One Account Customers
# -----------------------------------

for customer_id in one_account_customers:
    accounts.append(
        create_account(customer_id, account_number)
    )
    account_number += 1

# -----------------------------------
# Generate Two Account Customers
# -----------------------------------

for customer_id in two_account_customers:
    for _ in range(2):
        accounts.append(
            create_account(customer_id, account_number)
        )
        account_number += 1

# -----------------------------------
# Generate Three Account Customers
# -----------------------------------

for customer_id in three_account_customers:
    for _ in range(3):
        accounts.append(
            create_account(customer_id, account_number)
        )
        account_number += 1

# -----------------------------------
# Create DataFrame
# -----------------------------------

accounts_df = pd.DataFrame(accounts)

# -----------------------------------
# Validation
# -----------------------------------

assert len(accounts_df) == 65000
assert accounts_df["account_id"].is_unique
assert accounts_df["customer_id"].notnull().all()
assert accounts_df["branch_id"].notnull().all()

# Verify customer-account distribution

account_counts = accounts_df.groupby(
    "customer_id"
).size()

assert (account_counts == 1).sum() == 37500
assert (account_counts == 2).sum() == 10000
assert (account_counts == 3).sum() == 2500

# -----------------------------------
# Save CSV
# -----------------------------------

output_path = "generated_data/accounts.csv"

accounts_df.to_csv(
    output_path,
    index=False
)

# -----------------------------------
# Summary
# -----------------------------------

print("=" * 60)
print("Accounts Generation Completed")
print("=" * 60)

print(f"Total Accounts Generated : {len(accounts_df)}")
print()

print("Customer -> Account Distribution")
print(account_counts.value_counts().sort_index())
print()

print("Account Type Distribution")
print(accounts_df["account_type"].value_counts())
print()

print("Account Status Distribution")
print(accounts_df["status"].value_counts())
print()

print(f"CSV Saved Successfully : {output_path}")

print("=" * 60)
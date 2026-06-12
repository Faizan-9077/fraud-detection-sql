import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# -----------------------------------
# Configuration
# -----------------------------------

TOTAL_TRANSACTIONS = 499000

random.seed(42)
np.random.seed(42)

# -----------------------------------
# Load Data
# -----------------------------------

accounts_df = pd.read_csv(
    "generated_data/accounts.csv"
)

beneficiaries_df = pd.read_csv(
    "generated_data/beneficiaries.csv"
)

account_ids = accounts_df[
    "account_id"
].tolist()

# account -> beneficiaries

beneficiary_map = (
    beneficiaries_df
    .groupby("account_id")[
        "beneficiary_id"
    ]
    .apply(list)
    .to_dict()
)

# beneficiary -> country

country_map = (
    beneficiaries_df
    .set_index(
        "beneficiary_id"
    )[
        "country_id"
    ]
    .to_dict()
)

# live balances

balance_map = (
    accounts_df
    .set_index(
        "account_id"
    )[
        "balance"
    ]
    .to_dict()
)

# -----------------------------------
# Transaction Settings
# -----------------------------------

TRANSACTION_TYPES = [
    "CASH_DEPOSIT",
    "CASH_WITHDRAWAL",
    "UPI_TRANSFER",
    "NEFT",
    "RTGS",
    "IMPS",
    "SWIFT"
]

TRANSACTION_WEIGHTS = [
    0.20,
    0.15,
    0.30,
    0.15,
    0.08,
    0.07,
    0.05
]

CHANNELS = [
    "ATM",
    "BRANCH",
    "UPI",
    "MOBILE_BANKING",
    "INTERNET_BANKING",
    "SWIFT"
]

CHANNEL_WEIGHTS = [
    0.10,
    0.15,
    0.35,
    0.20,
    0.15,
    0.05
]

STATUS = [
    "SUCCESS",
    "FAILED",
    "PENDING"
]

STATUS_WEIGHTS = [
    0.96,
    0.03,
    0.01
]

# -----------------------------------
# Helper Functions
# -----------------------------------

def generate_amount():

    x = random.random()

    if x < 0.60:
        return round(
            random.uniform(
                500,
                10000
            ),
            2
        )

    elif x < 0.90:
        return round(
            random.uniform(
                10000,
                100000
            ),
            2
        )

    elif x < 0.98:
        return round(
            random.uniform(
                100000,
                500000
            ),
            2
        )

    else:
        return round(
            random.uniform(
                500000,
                1000000
            ),
            2
        )


def generate_datetime():

    start = datetime(
        2025,
        1,
        1
    )

    end = datetime(
        2026,
        6,
        1
    )

    seconds = int(
        (
            end - start
        ).total_seconds()
    )

    return (
        start +
        timedelta(
            seconds=random.randint(
                0,
                seconds
            )
        )
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# -----------------------------------
# Generate Transactions
# -----------------------------------

transactions = []

for i in range(
    1,
    TOTAL_TRANSACTIONS + 1
):

    account_id = random.choice(
        account_ids
    )

    beneficiary_id = random.choice(
        beneficiary_map[
            account_id
        ]
    )

    txn_type = random.choices(
        TRANSACTION_TYPES,
        weights=TRANSACTION_WEIGHTS,
        k=1
    )[0]

    amount = generate_amount()

    current_balance = balance_map[
        account_id
    ]

    debit_transactions = [

        "CASH_WITHDRAWAL",
        "UPI_TRANSFER",
        "NEFT",
        "RTGS",
        "IMPS",
        "SWIFT"

    ]

    if txn_type in debit_transactions:

        if current_balance >= amount:

            current_balance -= amount

        else:

            txn_type = "CASH_DEPOSIT"

            current_balance += amount

    else:

        current_balance += amount

    balance_map[
        account_id
    ] = current_balance

    transactions.append(

        {

            "txn_id":
            f"TXN{i:09d}",

            "account_id":
            account_id,

            "beneficiary_id":
            beneficiary_id,

            "txn_type":
            txn_type,

            "amount":
            amount,

            "balance_after_txn":
            round(
                current_balance,
                2
            ),

            "txn_time":
            generate_datetime(),

            "channel":
            random.choices(
                CHANNELS,
                weights=CHANNEL_WEIGHTS,
                k=1
            )[0],

            "country_id":
            country_map[
                beneficiary_id
            ],

            "device_id":
            f"DEV{random.randint(1,50000):06d}",

            "status":
            random.choices(
                STATUS,
                weights=STATUS_WEIGHTS,
                k=1
            )[0],

            "fraud_pattern":
            "NORMAL"

        }

    )

# -----------------------------------
# DataFrame
# -----------------------------------

transactions_df = pd.DataFrame(
    transactions
)

# -----------------------------------
# Validation
# -----------------------------------

assert len(
    transactions_df
) == 499000

assert transactions_df[
    "txn_id"
].is_unique

assert transactions_df[
    "amount"
].gt(
    0
).all()

assert transactions_df[
    "balance_after_txn"
].ge(
    0
).all()

# -----------------------------------
# Save
# -----------------------------------

output_path = (
    "generated_data/"
    "transactions_normal.csv"
)

transactions_df.to_csv(

    output_path,

    index=False

)

# -----------------------------------
# Summary
# -----------------------------------

print("=" * 60)
print(
    "Normal Transactions Generation Completed"
)
print("=" * 60)

print(
    f"Total Transactions : "
    f"{len(transactions_df)}"
)

print()

print(
    "Transaction Type Distribution"
)

print(
    transactions_df[
        "txn_type"
    ].value_counts()
)

print()

print(
    "Transaction Status Distribution"
)

print(
    transactions_df[
        "status"
    ].value_counts()
)

print()

print(
    f"CSV Saved Successfully : "
    f"{output_path}"
)

print("=" * 60)
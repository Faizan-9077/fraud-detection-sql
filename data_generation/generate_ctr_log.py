import pandas as pd

# -----------------------------------
# Configuration
# -----------------------------------

CTR_THRESHOLD = 100000

# -----------------------------------
# Load Data
# -----------------------------------

transactions_df = pd.read_csv(
    "generated_data/transactions.csv"
)

# -----------------------------------
# Filter CTR Transactions
# -----------------------------------

ctr_transactions = transactions_df[

    (

        transactions_df[
            "txn_type"
        ].isin(

            [
                "CASH_DEPOSIT",
                "CASH_WITHDRAWAL"
            ]

        )

    )

    &

    (

        transactions_df[
            "amount"
        ] >= CTR_THRESHOLD

    )

].copy()

# Include Pattern 7 Transactions

p7_transactions = transactions_df[

    transactions_df[
        "fraud_pattern"
    ] == "P7"

].copy()

ctr_transactions = pd.concat(

    [

        ctr_transactions,

        p7_transactions

    ]

)

ctr_transactions = ctr_transactions.drop_duplicates(

    subset="txn_id"

)

# -----------------------------------
# Generate CTR Logs
# -----------------------------------

ctr_logs = []

counter = 1

for _, row in ctr_transactions.iterrows():

    ctr_logs.append(

        {

            "ctr_id":
            f"CTR{counter:09d}",

            "account_id":
            row["account_id"],

            "txn_id":
            row["txn_id"],

            "amount":
            row["amount"],

            "txn_time":
            row["txn_time"]

        }

    )

    counter += 1

# -----------------------------------
# DataFrame
# -----------------------------------

ctr_df = pd.DataFrame(
    ctr_logs
)

# -----------------------------------
# Validation
# -----------------------------------

assert ctr_df[
    "ctr_id"
].is_unique

assert ctr_df[
    "account_id"
].notna().all()

assert ctr_df[
    "amount"
].gt(
    0
).all()

# -----------------------------------
# Save
# -----------------------------------

output_path = (

    "generated_data/"
    "ctr_log.csv"

)

ctr_df.to_csv(

    output_path,

    index=False

)

# -----------------------------------
# Summary
# -----------------------------------

print("=" * 60)
print(
    "CTR Log Generation Completed"
)
print("=" * 60)

print(
    f"Total CTR Records : "
    f"{len(ctr_df)}"
)

print()

print(
    f"CSV Saved Successfully : "
    f"{output_path}"
)

print("=" * 60)
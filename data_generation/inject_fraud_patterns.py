import random
import numpy as np
import pandas as pd
from datetime import timedelta


# ============================================================
# Configuration
# ============================================================

SEED = 42

DEFAULT_COUNTRY_ID = 1

CASH_STRUCTURING_ACCOUNTS = 20

MIN_STRUCTURING_TXNS = 6
MAX_STRUCTURING_TXNS = 8

MIN_STRUCTURING_AMOUNT = 150000
MAX_STRUCTURING_AMOUNT = 199999

STRUCTURING_WINDOW_HOURS = 72

random.seed(SEED)
np.random.seed(SEED)

# ============================================================
# Load Data
# ============================================================

def load_data():

    transactions_df = pd.read_csv(
        "generated_data/transactions_normal.csv"
    )

    accounts_df = pd.read_csv(
        "generated_data/accounts.csv"
    )

    beneficiaries_df = pd.read_csv(
        "generated_data/beneficiaries.csv"
    )

    fatf_df = pd.read_csv(
        "generated_data/fatf_high_risk_countries.csv"
    )

    return (
        transactions_df,
        accounts_df,
        beneficiaries_df,
        fatf_df
    )

def get_cash_structuring_accounts(accounts_df):

    active_accounts = accounts_df[
        accounts_df["status"] == "ACTIVE"
    ]

    selected_accounts = active_accounts.sample(
        n=CASH_STRUCTURING_ACCOUNTS,
        random_state=SEED
    )

    return selected_accounts["account_id"].tolist()


def generate_cash_structuring_transactions(
    account_id,
    start_txn_id
):

    fraud_transactions = []

    num_txns = random.randint(MIN_STRUCTURING_TXNS, MAX_STRUCTURING_TXNS)

    base_time = pd.Timestamp(
        "2025-01-01"
    ) + pd.Timedelta(
        days=random.randint(0, 300)
    )

    for i in range(num_txns):

        txn = {
            "txn_id": f"TXN{start_txn_id + i:09d}",
            "account_id": account_id,
            "beneficiary_id": np.nan,
            "txn_type": "CASH_DEPOSIT",
            "amount": random.randint(
                MIN_STRUCTURING_AMOUNT,
                MAX_STRUCTURING_AMOUNT
            ),
            "balance_after_txn": np.nan,
            "txn_time": base_time + timedelta(
                hours=random.randint(0, STRUCTURING_WINDOW_HOURS)
            ),
            "channel": "BRANCH",
            "country_id": DEFAULT_COUNTRY_ID,
            "device_id": np.nan,
            "status": "SUCCESS",
            "fraud_pattern": "CASH_STRUCTURING"
        }

        fraud_transactions.append(txn)

    return fraud_transactions


# ============================================================
# Fraud Pattern 1
# Cash Structuring
# ============================================================

def inject_cash_structuring(
    transactions_df,
    accounts_df
):

    print("\nInjecting Pattern 1 : Cash Structuring...")

    selected_accounts = get_cash_structuring_accounts(
        accounts_df
    )

    print(
        f"Selected {len(selected_accounts)} accounts."
    )

    if "fraud_pattern" not in transactions_df.columns:
        transactions_df["fraud_pattern"] = "NORMAL"

    last_txn_id = transactions_df["txn_id"].max()

    next_txn_id = int(
        last_txn_id.replace("TXN", "")
    ) + 1

    fraud_rows = []

    for account_id in selected_accounts:

        rows = generate_cash_structuring_transactions(
            account_id,
            next_txn_id
        )

        fraud_rows.extend(rows)

        next_txn_id += len(rows)

    fraud_df = pd.DataFrame(fraud_rows)

    transactions_df = pd.concat(
        [
            transactions_df,
            fraud_df
        ],
        ignore_index=True
    )

    print(
        f"Injected {len(fraud_df)} fraud transactions."
    )

    print("\nCash Structuring Validation")
    print("-" * 40)
    print(
        f"Unique Accounts : "
        f"{fraud_df['account_id'].nunique()}"
    )
    print(
        f"Total Transactions : "
        f"{len(fraud_df)}"
    )
    print(
        f"Minimum Amount : "
        f"{fraud_df['amount'].min()}"
    )
    print(
        f"Maximum Amount : "
        f"{fraud_df['amount'].max()}"
    )

    return transactions_df
# ============================================================
# Fraud Pattern 2
# Large Late Night Transactions
# ============================================================

def inject_large_late_night(
    transactions_df
):

    print("Injecting Pattern 2 : Large Late Night Transactions...")

    return transactions_df


# ============================================================
# Fraud Pattern 3
# Account Takeover
# ============================================================

def inject_account_takeover(
    transactions_df
):

    print("Injecting Pattern 3 : Account Takeover...")

    return transactions_df


# ============================================================
# Future Patterns
# ============================================================

def inject_round_tripping(
    transactions_df
):

    return transactions_df


def inject_cross_border_burst(
    transactions_df
):

    return transactions_df


def inject_dormant_reactivation(
    transactions_df
):

    return transactions_df


def inject_ctr_threshold_splitting(
    transactions_df
):

    return transactions_df


def inject_pep_activity(
    transactions_df
):

    return transactions_df


# ============================================================
# Save Data
# ============================================================

def save_data(transactions_df):

    transactions_df["txn_time"] = pd.to_datetime(
        transactions_df["txn_time"]
    )

    transactions_df = transactions_df.sort_values(
        by=["txn_time", "txn_id"]
    )

    transactions_df.reset_index(
        drop=True,
        inplace=True
    )

    transactions_df.to_csv(
        "generated_data/transactions.csv",
        index=False
    )

    print("\ntransactions.csv generated successfully.")

# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("Fraud Pattern Injection Started")
    print("=" * 60)

    (
        transactions_df,
        accounts_df,
        beneficiaries_df,
        fatf_df
    ) = load_data()

    # Pattern 1

    transactions_df = inject_cash_structuring(
        transactions_df,
        accounts_df
    )

    # Future Patterns

    # transactions_df = inject_large_late_night(
    #     transactions_df
    # )

    # transactions_df = inject_account_takeover(
    #     transactions_df
    # )

    save_data(transactions_df)

    print("=" * 60)
    print("Fraud Pattern Injection Completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
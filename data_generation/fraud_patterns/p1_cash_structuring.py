import random
import numpy as np
import pandas as pd

from datetime import timedelta

from fraud_patterns.common import *

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
    start_txn_id,
    accounts_df
):

    fraud_transactions = []

    current_balance = accounts_df.loc[
        accounts_df["account_id"] == account_id,
        "balance"
    ].iloc[0]

    num_txns = random.randint(MIN_STRUCTURING_TXNS, MAX_STRUCTURING_TXNS)

    base_time = pd.Timestamp(
        "2025-01-01"
    ) + pd.Timedelta(
        days=random.randint(0, 300)
    )

    for i in range(num_txns):

        txn_amount = random.randint(
            MIN_STRUCTURING_AMOUNT,
            MAX_STRUCTURING_AMOUNT
        )

        balance_after_txn = (
            current_balance + txn_amount
        )

        current_balance = balance_after_txn

        txn = {

            "txn_id":
            f"TXN{start_txn_id + i:09d}",

            "account_id":
            account_id,

            "beneficiary_id":
            np.nan,

            "txn_type":
            "CASH_DEPOSIT",

            "amount":
            txn_amount,

            "balance_after_txn":
            balance_after_txn,

            "txn_time":
            base_time + timedelta(
                hours=random.randint(
                    0,
                    STRUCTURING_WINDOW_HOURS
                )
            ),

            "channel":
            "BRANCH",

            "country_id":
            DEFAULT_COUNTRY_ID,

            "device_id":
            np.nan,

            "status":
            "SUCCESS",

            "fraud_pattern":
            "CASH_STRUCTURING"

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
            next_txn_id,
            accounts_df
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
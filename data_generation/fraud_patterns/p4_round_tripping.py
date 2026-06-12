import random
import uuid
from datetime import timedelta

import pandas as pd

from fraud_patterns.common import RANDOM_SEED

random.seed(RANDOM_SEED)


def inject_round_tripping(transactions_df, accounts_df):

    active_accounts = accounts_df[
        accounts_df["status"] == "ACTIVE"
    ]["account_id"].tolist()

    selected_accounts = random.sample(
        active_accounts,
        min(20, len(active_accounts))
    )

    fraud_transactions = []

    last_id = (
        transactions_df["txn_id"]
        .str.replace("TXN", "", regex=False)
        .astype(int)
        .max()
    )

    transaction_counter = last_id + 1

    for source_account in selected_accounts:

        chain_length = random.randint(3, 4)

        possible_accounts = [
            acc for acc in active_accounts
            if acc != source_account
        ]

        chain_members = random.sample(
            possible_accounts,
            chain_length - 1
        )

        chain = [source_account] + chain_members
        chain.append(source_account)

        base_amount = random.randint(
            250000,
            800000
        )

        start_time = pd.to_datetime(
            transactions_df["txn_time"]
        ).sample(1).iloc[0]

        for i in range(len(chain) - 1):

            sender = chain[i]
            receiver = chain[i + 1]

            amount = (
                base_amount
                - random.randint(500, 3000) * i
            )

            txn = {
                "txn_id": f"TXN{transaction_counter:09d}",

                "account_id": sender,

                "beneficiary_id": f"BEN{random.randint(1, 99999):08d}",

                "txn_type": random.choice(
                    [
                        "NEFT",
                        "RTGS"
                    ]
                ),

                "amount": amount,

                "balance_after_txn": 0.0,

                "txn_time": start_time + timedelta(
                    minutes=random.randint(15, 90) * (i + 1)
                ),

                "channel": "INTERNET_BANKING",

                "country_id": 20,

                "device_id": str(uuid.uuid4())[:12],

                "status": "SUCCESS",

                "fraud_pattern": "ROUND_TRIPPING"
            }

            fraud_transactions.append(txn)

            transaction_counter += 1

    fraud_df = pd.DataFrame(
        fraud_transactions
    )

    validate_round_tripping(
        fraud_df,
        len(selected_accounts)
    )

    final_df = pd.concat(
        [
            transactions_df,
            fraud_df
        ],
        ignore_index=True
    )

    final_df = pd.concat(
        [
            transactions_df,
            fraud_df
        ],
        ignore_index=True
    )

    return final_df


def validate_round_tripping(
    fraud_df,
    total_chains
):

    print("\nRound Tripping Validation")
    print("-" * 40)

    print(
        f"Unique Chains : {total_chains}"
    )

    print(
        f"Fraud Transactions : "
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
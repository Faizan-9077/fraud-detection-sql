import random
import uuid
from datetime import timedelta

import pandas as pd

from fraud_patterns.common import RANDOM_SEED

random.seed(RANDOM_SEED)


def inject_cross_border_burst(
    transactions_df,
    accounts_df,
    fatf_df
):

    transactions_df["txn_time"] = pd.to_datetime(
        transactions_df["txn_time"]
    )

    active_accounts = accounts_df[
        accounts_df["status"] == "ACTIVE"
    ]["account_id"].tolist()

    selected_accounts = random.sample(
        active_accounts,
        min(15, len(active_accounts))
    )

    high_risk_country_ids = fatf_df[
        "country_id"
    ].tolist()

    fraud_transactions = []

    last_id = (
        transactions_df["txn_id"]
        .str.replace(
            "TXN",
            "",
            regex=False
        )
        .astype(int)
        .max()
    )

    transaction_counter = last_id + 1

    for account in selected_accounts:

        number_of_transactions = random.randint(
            3,
            6
        )

        start_time = random.choice(
            transactions_df["txn_time"].tolist()
        )

        for i in range(
            number_of_transactions
        ):

            txn = {

                "txn_id":
                f"TXN{transaction_counter:09d}",

                "account_id":
                account,

                "beneficiary_id":
                f"BEN{random.randint(1,99999):08d}",

                "txn_type":
                random.choice(
                    [
                        "NEFT",
                        "RTGS"
                    ]
                ),

                "amount":
                random.randint(
                    500000,
                    3000000
                ),

                "balance_after_txn":
                0.0,

                "txn_time":
                start_time
                + timedelta(
                    minutes=15 * (i + 1)
                ),

                "channel":
                "INTERNET_BANKING",

                "country_id":
                random.choice(
                    high_risk_country_ids
                ),

                "device_id":
                str(
                    uuid.uuid4()
                )[:12],

                "status":
                "SUCCESS",

                "fraud_pattern":
                "CROSS_BORDER_BURST"

            }

            fraud_transactions.append(
                txn
            )

            transaction_counter += 1

    fraud_df = pd.DataFrame(
        fraud_transactions
    )

    validate_cross_border_burst(
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

    return final_df

def validate_cross_border_burst(
    fraud_df,
    total_accounts
):

    print(
        "\nCross Border Burst Validation"
    )

    print(
        "-" * 40
    )

    print(
        f"Unique Accounts : "
        f"{total_accounts}"
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

    print(
        f"Countries Involved : "
        f"{fraud_df['country_id'].nunique()}"
    )
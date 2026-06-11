import random
import uuid
from datetime import timedelta

import pandas as pd

from fraud_patterns.common import RANDOM_SEED

random.seed(RANDOM_SEED)


def inject_pep_activity(
    transactions_df,
    accounts_df
):

    transactions_df["txn_time"] = pd.to_datetime(
        transactions_df["txn_time"]
    )

    active_accounts = accounts_df[
        accounts_df["status"] == "ACTIVE"
    ]["account_id"].tolist()

    selected_accounts = random.sample(
        active_accounts,
        min(10, len(active_accounts))
    )

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

        start_time = random.choice(
            transactions_df["txn_time"].tolist()
        )

        number_of_transactions = random.randint(
            2,
            4
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
                        "RTGS",
                        "NEFT"
                    ]
                ),

                "amount":
                random.randint(
                    2000000,
                    5000000
                ),

                "balance_after_txn":
                0.0,

                "txn_time":
                start_time
                + timedelta(
                    hours=i
                ),

                "channel":
                "INTERNET_BANKING",

                "country_id":
                1,

                "device_id":
                str(
                    uuid.uuid4()
                )[:12],

                "status":
                "SUCCESS",

                "fraud_pattern":
                "P8_PEP_ACTIVITY"

            }

            fraud_transactions.append(
                txn
            )

            transaction_counter += 1

    fraud_df = pd.DataFrame(
        fraud_transactions
    )

    validate_pep_activity(
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


def validate_pep_activity(
    fraud_df,
    total_accounts
):

    print(
        "\nPEP Suspicious Activity Validation"
    )

    print(
        "-" * 40
    )

    print(
        f"Unique Accounts : {total_accounts}"
    )

    print(
        f"Fraud Transactions : {len(fraud_df)}"
    )

    print(
        f"Minimum Amount : {fraud_df['amount'].min()}"
    )

    print(
        f"Maximum Amount : {fraud_df['amount'].max()}"
    )
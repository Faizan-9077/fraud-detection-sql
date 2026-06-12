import random
import uuid
from datetime import timedelta

import pandas as pd

from fraud_patterns.common import RANDOM_SEED

random.seed(RANDOM_SEED)


def inject_dormant_reactivation(
    transactions_df,
    accounts_df
):

    transactions_df["txn_time"] = pd.to_datetime(
        transactions_df["txn_time"]
    )

    last_transaction = (
        transactions_df
        .groupby("account_id")["txn_time"]
        .max()
        .reset_index()
    )

    dataset_end = transactions_df[
        "txn_time"
    ].max()

    last_transaction["days_inactive"] = (
        dataset_end
        - last_transaction["txn_time"]
    ).dt.days

    eligible_accounts = last_transaction[
        last_transaction["days_inactive"] >= 90
    ]["account_id"].tolist()

    selected_accounts = random.sample(
        eligible_accounts,
        min(20, len(eligible_accounts))
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

    last_transaction = (
        transactions_df
        .groupby("account_id")["txn_time"]
        .max()
        .to_dict()
    )

    for account in selected_accounts:

        number_of_transactions = random.randint(
            2,
            4
        )

        if account in last_transaction:

            dormant_days = random.randint(
                90,
                180
            )

            reactivation_time = (
                last_transaction[account]
                + timedelta(days=dormant_days)
            )

        else:

            reactivation_time = random.choice(
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
                        "RTGS",
                        "IMPS"
                    ]
                ),

                "amount":
                random.randint(
                    250000,
                    1000000
                ),

                "balance_after_txn":
                0.0,

                "txn_time":
                reactivation_time
                + timedelta(
                    minutes=30 * i
                ),

                "channel":
                random.choice(
                    [
                        "INTERNET_BANKING",
                        "MOBILE_BANKING"
                    ]
                ),

                "country_id":
                1,

                "device_id":
                str(
                    uuid.uuid4()
                )[:12],

                "status":
                "SUCCESS",

                "fraud_pattern":
                "DORMANT_REACTIVATION"

            }

            fraud_transactions.append(
                txn
            )

            transaction_counter += 1

    fraud_df = pd.DataFrame(
        fraud_transactions
    )

    validate_dormant_reactivation(
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


def validate_dormant_reactivation(
    fraud_df,
    total_accounts
):

    print(
        "\nDormant Account Reactivation Validation"
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
        f"Channels Used : "
        f"{fraud_df['channel'].nunique()}"
    )
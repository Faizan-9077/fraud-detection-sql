import random
import uuid
from datetime import timedelta

import pandas as pd

from fraud_patterns.common import RANDOM_SEED

random.seed(RANDOM_SEED)


def inject_pep_activity(
    transactions_df,
    accounts_df,
    beneficiaries_df
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

    beneficiary_lookup = (
        beneficiaries_df
        .groupby("account_id")["beneficiary_id"]
        .apply(list)
        .to_dict()
    )


    for account in selected_accounts:

        current_balance = accounts_df.loc[
            accounts_df["account_id"] == account,
            "balance"
        ].iloc[0]

    
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
            
            txn_amount = random.randint(
                2000000,
                5000000
            )

            balance_after_txn = max(
                current_balance - txn_amount,
                0
            )

            current_balance = balance_after_txn

            available_beneficiaries = beneficiary_lookup.get(
                account,
                []
            )

            beneficiary_id = random.choice(
                available_beneficiaries
            )

            txn = {

                "txn_id":
                f"TXN{transaction_counter:09d}",

                "account_id":
                account,

                "beneficiary_id":
                beneficiary_id,

                "txn_type":
                random.choice(
                    [
                        "RTGS",
                        "NEFT"
                    ]
                ),

                "amount":
                txn_amount,

                "balance_after_txn":
                balance_after_txn,

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
                "PEP_ACTIVITY"

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
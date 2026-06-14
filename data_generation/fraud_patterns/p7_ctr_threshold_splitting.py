import random
import uuid
from datetime import timedelta

import pandas as pd

from fraud_patterns.common import RANDOM_SEED

random.seed(RANDOM_SEED)


def inject_ctr_threshold_splitting(
    transactions_df,
    accounts_df,
    beneficiaries_df
):

    transactions_df["txn_time"] = pd.to_datetime(
        transactions_df["txn_time"]
    )

    beneficiary_lookup = (
        beneficiaries_df
        .groupby("account_id")["beneficiary_id"]
        .apply(list)
        .to_dict()
    )

    account_balance_lookup = (
        accounts_df
        .set_index("account_id")["balance"]
        .to_dict()
    )

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
            3,
            5
        )

        for i in range(
            number_of_transactions
        ):
            
            available_beneficiaries = beneficiary_lookup.get(
                account,
                []
            )

            beneficiary_id = random.choice(
                available_beneficiaries
            )

            current_balance = account_balance_lookup.get(
                account,
                0
            )

            txn_amount = random.randint(
                950000,
                999999
            )

            balance_after_txn = (
                current_balance + txn_amount
            )

            account_balance_lookup[account] = (
                balance_after_txn
            )

            txn = {

                "txn_id":
                f"TXN{transaction_counter:09d}",

                "account_id":
                account,

                "beneficiary_id":
                beneficiary_id,

                "txn_type":
                "CASH_DEPOSIT",

                "amount":
                txn_amount,

                "balance_after_txn":
                balance_after_txn,

                "txn_time":
                start_time
                + timedelta(
                    minutes=20 * i
                ),

                "channel":
                "BRANCH",

                "country_id":
                1,

                "device_id":
                str(
                    uuid.uuid4()
                )[:12],

                "status":
                "SUCCESS",

                "fraud_pattern":
                "CTR_THRESHOLD_SPLITTING"

            }

            fraud_transactions.append(
                txn
            )

            transaction_counter += 1

    fraud_df = pd.DataFrame(
        fraud_transactions
    )

    validate_ctr_threshold_splitting(
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


def validate_ctr_threshold_splitting(
    fraud_df,
    total_accounts
):

    print(
        "\nCTR Threshold Splitting Validation"
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
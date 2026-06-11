import pandas as pd

from fraud_patterns.p1_cash_structuring import (
    inject_cash_structuring
)

from fraud_patterns.p2_large_late_night import (
    inject_large_late_night
)

from fraud_patterns.p3_account_takeover import (
    inject_account_takeover
)
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

    transactions_df = inject_large_late_night(
    transactions_df,
    accounts_df
    )

    transactions_df = inject_account_takeover(
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
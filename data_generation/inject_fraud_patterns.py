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

from fraud_patterns.p4_round_tripping import (
    inject_round_tripping
)

from fraud_patterns.p5_cross_border_burst import (
    inject_cross_border_burst
)

from fraud_patterns.p6_dormant_reactivation import (
    inject_dormant_reactivation
)

from fraud_patterns.p7_ctr_threshold_splitting import (
    inject_ctr_threshold_splitting
)

from fraud_patterns.p8_pep_activity import (
    inject_pep_activity
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

    transactions_df["country_id"] = (
        pd.to_numeric(
            transactions_df["country_id"],
            errors="coerce"
        )
        .astype("Int64")
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
        fatf_countries
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

    transactions_df = inject_round_tripping(
        transactions_df,
        accounts_df,
        beneficiaries_df,
        fatf_countries
    )

    transactions_df = inject_cross_border_burst(
        transactions_df,
        accounts_df,
        beneficiaries_df,
        fatf_countries
    )

    transactions_df = inject_dormant_reactivation(
        transactions_df,
        accounts_df,
        beneficiaries_df
    )

    transactions_df = inject_ctr_threshold_splitting(
        transactions_df,
        accounts_df,
        beneficiaries_df
    )

    transactions_df = inject_pep_activity(
        transactions_df,
        accounts_df,
        beneficiaries_df
    )



    save_data(transactions_df)

    print("=" * 60)
    print("Fraud Pattern Injection Completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
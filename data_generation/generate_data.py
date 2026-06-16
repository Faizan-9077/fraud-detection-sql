import subprocess
import sys


def run_script(script_name):

    print("\n" + "=" * 60)
    print(f"Running {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script_name]
    )

    if result.returncode != 0:

        print(
            f"\nError while executing {script_name}"
        )

        sys.exit(1)


def main():

    print("\n")
    print("=" * 60)
    print("Synthetic Banking Dataset Generation Started")
    print("=" * 60)

    scripts = [

        "data_generation/generate_branches.py",

        "data_generation/generate_customers.py",

        "data_generation/generate_accounts.py",

        "data_generation/generate_fatf_high_risk_countries.py",

        "data_generation/generate_beneficiaries.py",

        "data_generation/generate_kyc_records.py",

        "data_generation/generate_device_logins.py",

        "data_generation/generate_transactions.py",

        "data_generation/inject_fraud_patterns.py",

        "data_generation/generate_aml_alerts.py",

        "data_generation/generate_ctr_log.py"

    ]

    for script in scripts:

        run_script(script)

    print("\n")
    print("=" * 60)
    print("Synthetic Banking Dataset Generation Completed")
    print("=" * 60)


if __name__ == "__main__":

    main()
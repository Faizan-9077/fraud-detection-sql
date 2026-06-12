import os
import psycopg2

from database.db_config import DB_CONFIG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(
    BASE_DIR,
    "generated_data"
)

TABLE_FILES = [
    ("branches", "branches.csv"),
    ("customers", "customers.csv"),
    ("fatf_high_risk_countries", "fatf_high_risk_countries.csv"),
    ("accounts", "accounts.csv"),
    ("kyc_records", "kyc_records.csv"),
    ("beneficiaries", "beneficiaries.csv"),
    ("device_logins", "device_logins.csv"),
    ("transactions", "transactions.csv"),
    ("aml_alerts", "aml_alerts.csv"),
    ("ctr_log", "ctr_log.csv")
]


def load_table(cursor, table_name, file_name):

    file_path = os.path.join(DATA_DIR, file_name)

    with open(file_path, "r", encoding="utf-8") as file:

        cursor.copy_expert(
            f"""
            COPY {table_name}
            FROM STDIN
            WITH CSV HEADER
            """,
            file
        )

    print(f"Loaded {table_name}")


def main():

    connection = psycopg2.connect(**DB_CONFIG)

    cursor = connection.cursor()

    print("=" * 50)
    print("Database Loading Started")
    print("=" * 50)

    try:

        for table_name, file_name in TABLE_FILES:
            load_table(
                cursor,
                table_name,
                file_name
            )

        connection.commit()

        print("\nDatabase Loading Completed Successfully")

    except Exception as e:

        connection.rollback()

        print("\nError:")
        print(e)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
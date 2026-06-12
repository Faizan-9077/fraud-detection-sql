from faker import Faker
import pandas as pd
import random
import numpy as np
import os
from datetime import date

# ---------------------------------
# Setup
# ---------------------------------

fake = Faker()

SEED = 42

Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = "generated_data"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "fatf_high_risk_countries.csv"
)

# ---------------------------------
# FATF Master Data
# ---------------------------------

FATF_COUNTRIES = [
    ("Iran", "IRN", "HIGH", "BLACK", "ACTIVE", 100),
    ("North Korea", "PRK", "HIGH", "BLACK", "ACTIVE", 100),
    ("Myanmar", "MMR", "HIGH", "GREY", "ACTIVE", 95),
    ("Syria", "SYR", "HIGH", "GREY", "ACTIVE", 95),
    ("Yemen", "YEM", "HIGH", "GREY", "ACTIVE", 94),
    ("Pakistan", "PAK", "MEDIUM", "GREY", "ACTIVE", 90),
    ("Nigeria", "NGA", "MEDIUM", "GREY", "ACTIVE", 88),
    ("South Sudan", "SSD", "MEDIUM", "GREY", "ACTIVE", 87),
    ("Haiti", "HTI", "MEDIUM", "GREY", "ACTIVE", 86),
    ("Lebanon", "LBN", "MEDIUM", "GREY", "ACTIVE", 85),
    ("Monaco", "MCO", "MEDIUM", "GREY", "ACTIVE", 84),
    ("South Africa", "ZAF", "MEDIUM", "GREY", "ACTIVE", 83),
    ("Bulgaria", "BGR", "MEDIUM", "GREY", "ACTIVE", 82),
    ("Croatia", "HRV", "MEDIUM", "GREY", "ACTIVE", 81),
    ("Vietnam", "VNM", "MEDIUM", "GREY", "ACTIVE", 80),
    ("Kenya", "KEN", "MEDIUM", "GREY", "ACTIVE", 79),
    ("Mozambique", "MOZ", "MEDIUM", "GREY", "ACTIVE", 78),
    ("Congo", "COG", "MEDIUM", "GREY", "ACTIVE", 77),
    ("Uganda", "UGA", "MEDIUM", "GREY", "ACTIVE", 76),
    ("Cambodia", "KHM", "MEDIUM", "GREY", "ACTIVE", 75)
]

# ---------------------------------
# Generate Dataset
# ---------------------------------

def generate_country_data():

    countries = []

    for idx, country in enumerate(FATF_COUNTRIES, start=1):

        record = {
            "country_id": idx,
            "country_name": country[0],
            "iso_country_code": country[1],
            "risk_level": country[2],
            "fatf_list_type": country[3],
            "monitoring_status": country[4],
            "risk_score": country[5],
            "last_updated": date(2025, 1, 1),
            "remark": "Enhanced AML monitoring required"
        }

        countries.append(record)

    return pd.DataFrame(countries)


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = generate_country_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(df.head())

    print("\nTotal Countries Generated:")
    print(len(df))

    print(f"\nData saved to: {OUTPUT_FILE}")

    # ---------------------------------
    # Data Validation
    # ---------------------------------

    print("\nDuplicate Country IDs:")
    print(df["country_id"].duplicated().sum())

    print("\nDuplicate ISO Codes:")
    print(df["iso_country_code"].duplicated().sum())
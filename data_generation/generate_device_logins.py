import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# -----------------------------------
# Configuration
# -----------------------------------

random.seed(42)
np.random.seed(42)

MIN_LOGINS = 1
MAX_LOGINS = 5

# -----------------------------------
# Load Data
# -----------------------------------

customers_df = pd.read_csv(
    "generated_data/customers.csv"
)

fatf_df = pd.read_csv(
    "generated_data/fatf_high_risk_countries.csv"
)

customer_ids = customers_df[
    "customer_id"
].tolist()

fatf_country_ids = fatf_df[
    "country_id"
].tolist()

# -----------------------------------
# Helper Functions
# -----------------------------------

def generate_datetime():

    start = datetime(
        2025,
        1,
        1
    )

    end = datetime(
        2026,
        6,
        1
    )

    total_seconds = int(
        (
            end - start
        ).total_seconds()
    )

    return (
        start +
        timedelta(
            seconds=random.randint(
                0,
                total_seconds
            )
        )
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def generate_ip():

    return (
        f"{random.randint(1,223)}."
        f"{random.randint(0,255)}."
        f"{random.randint(0,255)}."
        f"{random.randint(1,254)}"
    )


def generate_country():

    x = random.random()

    # Domestic Login

    if x < 0.92:

        return None

    # Normal Foreign Login

    elif x < 0.98:

        return random.randint(
            21,
            100
        )

    # FATF High Risk Country

    else:

        return random.choice(
            fatf_country_ids
        )


# -----------------------------------
# Generate Device Logins
# -----------------------------------

device_logins = []

login_counter = 1

for customer_id in customer_ids:

    number_of_logins = random.randint(
        MIN_LOGINS,
        MAX_LOGINS
    )

    primary_device = (
        f"DEV{random.randint(1,50000):06d}"
    )

    secondary_device = (
        f"DEV{random.randint(1,50000):06d}"
    )

    for _ in range(
        number_of_logins
    ):

        if random.random() < 0.85:

            device_id = primary_device

        else:

            device_id = secondary_device

        device_logins.append(

            {

                "login_id":
                f"LOGIN{login_counter:09d}",

                "customer_id":
                customer_id,

                "device_id":
                device_id,

                "ip_address":
                generate_ip(),

                "country_id":
                generate_country(),

                "login_time":
                generate_datetime()

            }

        )

        login_counter += 1

# -----------------------------------
# DataFrame
# -----------------------------------

device_logins_df = pd.DataFrame(
    device_logins
)

device_logins_df["country_id"] = (
    device_logins_df["country_id"]
    .astype("Int64")
)

# -----------------------------------
# Validation
# -----------------------------------

assert device_logins_df[
    "login_id"
].is_unique

assert device_logins_df[
    "customer_id"
].notna().all()

assert device_logins_df[
    "device_id"
].notna().all()

assert device_logins_df[
    "ip_address"
].notna().all()

# -----------------------------------
# Save
# -----------------------------------

output_path = (
    "generated_data/"
    "device_logins.csv"
)

device_logins_df.to_csv(

    output_path,

    index=False

)

# -----------------------------------
# Summary
# -----------------------------------

print("=" * 60)
print(
    "Device Logins Generation Completed"
)
print("=" * 60)

print(
    f"Total Login Records : "
    f"{len(device_logins_df)}"
)

print()

print(
    "Country Distribution"
)

print(
    device_logins_df[
        "country_id"
    ].value_counts(
        dropna=False
    ).head(10)
)

print()

print(
    f"CSV Saved Successfully : "
    f"{output_path}"
)

print("=" * 60)
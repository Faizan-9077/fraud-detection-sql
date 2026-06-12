from faker import Faker
import pandas as pd
import random
import numpy as np
import os

# ---------------------------------
# Setup
# ---------------------------------

fake = Faker("en_IN")

SEED = 42

Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = "generated_data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "branches.csv")

# ---------------------------------
# Master Data
# ---------------------------------

BRANCH_TYPES = [
    "Main Branch",
    "City Branch",
    "Central Branch",
    "Commercial Branch",
    "Regional Branch"
]

CITY_STATE = {
    "Mumbai": "Maharashtra",
    "Delhi": "Delhi",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Pune": "Maharashtra",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh",
    "Bhopal": "Madhya Pradesh",
    "Patna": "Bihar",
    "Chandigarh": "Chandigarh",
    "Indore": "Madhya Pradesh",
    "Nagpur": "Maharashtra",
    "Kochi": "Kerala",
    "Surat": "Gujarat",
    "Kanpur": "Uttar Pradesh",
    "Noida": "Uttar Pradesh",
    "Guwahati": "Assam"
}

# ---------------------------------
# Helper Functions
# ---------------------------------

def generate_ifsc(branch_number):
    return f"ACCB0{branch_number:06d}"


# ---------------------------------
# Generate Branch Dataset
# ---------------------------------

def generate_branch_data():

    branches = []
    branch_number = 1

    for city, state in CITY_STATE.items():

        for branch_type in BRANCH_TYPES:

            branch = {
                "branch_id": generate_ifsc(branch_number),
                "branch_name": f"{city} {branch_type}",
                "city": city,
                "state": state
            }

            branches.append(branch)

            branch_number += 1

    return pd.DataFrame(branches)


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = generate_branch_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(df.head())

    print("\nTotal Branches Generated:")
    print(len(df))

    print(f"\nBranch data saved to: {OUTPUT_FILE}")

    # ---------------------------------
    # Data Validation
    # ---------------------------------

    print("\nDuplicate IFSC Codes:")
    print(df["branch_id"].duplicated().sum())

    print("\nDuplicate Branch Names:")
    print(df["branch_name"].duplicated().sum())
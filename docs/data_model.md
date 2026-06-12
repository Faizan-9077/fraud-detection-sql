# Database Relationship Diagram

```text
Customers
    |
    +------ Accounts
    |            |
    |            +------ Transactions
    |            |
    |            +------ Beneficiaries
    |
    +------ Device Logins
    |
    +------ KYC Records

Accounts
    |
    +------ AML Alerts
    |
    +------ CTR Log

Branches
    |
    +------ Accounts

FATF High Risk Countries
        |
        +------ Beneficiaries
        |
        +------ Transactions
```

---

## 1. Customers

Purpose:

Store customer master information.

Rows: 50,000

Primary Key:

* customer_id (CIF Number)

Columns:

* customer_id
* first_name
* middle_name
* last_name
* dob
* pan_number
* aadhar
* phone_number
* email
* risk_rating
* created_at

---

## 2. Branches

Purpose:

Store bank branch information.

Rows: 100

Primary Key:

* branch_id (IFSC Code)

Columns:

* branch_id
* branch_name
* city
* state

---

## 3. Accounts

Purpose:

Store customer bank accounts.

Rows: Approximately 65,000

Primary Key:

* account_id (Bank Account Number)

Foreign Keys:

* customer_id → Customers
* branch_id → Branches

Columns:

* account_id
* customer_id
* branch_id
* account_type
* balance
* status
* last_active_date

---

## Data Generation Order

1. Branches
2. FATF High Risk Countries
3. Customers
4. KYC Records
5. Accounts
6. Beneficiaries
7. Transactions
8. Device Logins
9. AML Alerts
10. CTR Log

---

## Development Workflow

```text
Master Data Generation
        |
        +---- Branches
        |
        +---- FATF High Risk Countries
        |
        +---- Customers
                    |
                    +---- KYC Records
                    |
                    +---- Accounts
                              |
                              +---- Beneficiaries
                              |
                              +---- Transactions
                              |
                              +---- AML Alerts
                              |
                              +---- CTR Log

CSV Files
        |
        V
PostgreSQL Database
        |
        V
LLaMA 3 NL to SQL
        |
        V
Fraud Investigation UI
        |
        V
SAR Evidence Generation
```

---

# Notes

* Data generation must be deterministic.
* Random seeds must be fixed.
* Fraud patterns should be intentionally embedded.
* Generated data should support natural language fraud investigation queries.
* Generated datasets must be compatible with the PostgreSQL schema.
* PAN numbers should be unique.
* Aadhaar numbers should be unique.
* Phone numbers should be unique.
* Email addresses should be unique.
* Customer IDs should use CIF format.
* Branch IDs should use IFSC format.
* Account IDs should represent actual bank account numbers.
* Master tables should be generated before dependent tables.

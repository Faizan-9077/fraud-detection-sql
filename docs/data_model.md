# Fraud Detection & Compliance Reporting Dataset Design

## 📑 Table of Contents
1. [Overview](#1-overview)
2. [Data Dictionary](#2-data-dictionary)
    - [customers](#21-customers)
    - [branches](#22-branches)
    - [fatf_high_risk_countries](#23-fatf_high_risk_countries)
    - [accounts](#24-accounts)
    - [kyc_records](#25-kyc_records)
    - [beneficiaries](#26-beneficiaries)
    - [device_logins](#27-device_logins)
    - [transactions](#28-transactions)
    - [aml_alerts](#29-aml_alerts)
    - [ctr_log](#210-ctr_log)

---

## 1. Overview
This schema is designed for a **Core Banking System** with integrated **Anti-Money Laundering (AML)** and **Know Your Customer (KYC)** monitoring capabilities. 

It tracks banking operations from customer onboarding and account management to transactional processing. It features strict data integrity constraints (Regex validations for CIFs, PAN, IFSC codes) and tracks high-risk geographical data, device logins, and automated AML / CTR (Currency Transaction Report) alerts.

---

## 2. Data Dictionary

### 2.1 `customers`
Stores core identity and contact details of the bank's customers.

| Column Name | Data Type | Properties / Constraints | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | `VARCHAR(20)` | **PK**, Not Null | Unique CIF identifier. |
| `first_name` | `VARCHAR(50)` | Not Null | Customer's first name. |
| `last_name` | `VARCHAR(50)` | Nullable | Customer's last name. |
| `middle_name` | `VARCHAR(50)` | Nullable | Customer's middle name. |
| `dob` | `DATE` | Not Null | Date of birth. |
| `pan_number` | `VARCHAR(10)` | **UNIQUE**, Not Null | Permanent Account Number. |
| `aadhar` | `VARCHAR(12)` | **UNIQUE**, Not Null | 12-digit Aadhar number. |
| `phone_number` | `VARCHAR(10)` | Not Null | 10-digit mobile number. |
| `email` | `VARCHAR(255)` | **UNIQUE** | Email address. |
| `risk_rating` | `VARCHAR(20)` | Default: `'LOW'` | Customer risk profile. |
| `created_at` | `TIMESTAMPTZ` | Default: `CURRENT_TIMESTAMP` | Account creation timestamp. |

**Constraints:**
- `chk_customer_no_space`: `customer_id` cannot contain spaces.
- `chk_customer_only_alphabet`: Names can only contain alphabets and spaces.
- `chk_customer_only_number`: `phone_number` exactly 10 digits; `aadhar` exactly 12 digits.
- `chk_pan_valid`: Standard Indian PAN format (`[A-Z]{5}[0-9]{4}[A-Z]`).

**Indexes:** 
- `idx_customers_risk_rating`

---

### 2.2 `branches`
Stores physical bank branch details.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `branch_id` | `VARCHAR(11)` | **PK**, Not Null | IFSC Code of the branch. |
| `branch_name` | `VARCHAR(50)` | Not Null | Name of the branch. |
| `city` | `VARCHAR(50)` | Not Null | City location. |
| `state` | `VARCHAR(50)` | Not Null | State location. |

**Constraints:**
- `chk_branch_id_valid`: Validates standard IFSC code format (`[A-Z]{4}0[A-Z0-9]{6}`).
- `chk_branch_only_alphabet`: Branch Name, City, and State must be alphabetic.

---

### 2.3 `fatf_high_risk_countries`
Maintains a list of countries flagged by the FATF for AML/CFT risks.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `country_id` | `INT` | **PK**, Not Null | Internal country ID. |
| `country_name` | `VARCHAR(50)` | Not Null | Name of the country. |
| `iso_country_code` | `CHAR(3)` | **UNIQUE**, Not Null | 3-letter ISO code. |
| `risk_level` | `VARCHAR(10)` | Not Null | e.g., 'HIGH', 'MEDIUM'. |
| `fatf_list_type` | `VARCHAR(10)` | Nullable | e.g., 'GREY', 'BLACK'. |
| `monitoring_status`| `VARCHAR(50)` | Not Null | Status of monitoring rules. |
| `risk_score` | `INT` | Not Null | Numerical risk score. |
| `last_updated` | `DATE` | Not Null | Last review date. |
| `remark` | `TEXT` | Nullable | Additional notes. |

**Constraints:**
- `chk_countries_only_alphabet`: Country name, ISO code, and risk level alphabetic only.
- `chk_risk_score`: `risk_score` >= 0.

---

### 2.4 `accounts`
Stores specific bank accounts belonging to customers.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `account_id` | `VARCHAR(20)` | **PK**, Not Null | Unique account number. |
| `customer_id` | `VARCHAR(20)` | **FK**, Not Null | Links to `customers`. |
| `branch_id` | `VARCHAR(11)` | **FK**, Not Null | Links to `branches`. |
| `account_type` | `VARCHAR(50)` | Not Null | e.g., Savings, Current. |
| `balance` | `NUMERIC(18,2)`| Default: `0.00` | Current account balance. |
| `status` | `VARCHAR(20)` | Default: `'ACTIVE'` | Account status. |
| `last_active_date` | `DATE` | Nullable | Last date of activity. |

**Constraints:**
- `fk_accounts_customer`: References `customers(customer_id)`.
- `fk_accounts_branch`: References `branches(branch_id)`.
- `chk_accounts_no_space`: No spaces in `account_id` or `customer_id`.
- `chk_accounts_id_valid`: `branch_id` must match IFSC format.
- `chk_accounts_only_alphabet`: `account_type` and `status` alphabetic only.

**Indexes:** 
- `idx_accounts_customer_id`
- `idx_accounts_branch_id`
- `idx_accounts_status`

---

### 2.5 `kyc_records`
Tracks the Know Your Customer (KYC) validation status for customers.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `kyc_id` | `BIGINT` | **PK**, Not Null | Unique KYC record ID. |
| `customer_id` | `VARCHAR(20)` | **FK**, Nullable | Links to `customers`. |
| `status` | `VARCHAR(50)` | Not Null | e.g., 'VERIFIED', 'PENDING'. |
| `review_date` | `DATE` | Not Null | Date KYC was reviewed. |

**Constraints:**
- `fk_kyc_customer`: References `customers(customer_id)`.
- `chk_kyc_no_space`: No spaces in `customer_id`.
- `chk_kyc_only_alphabet`: `status` must be alphabetic.

**Indexes:** 
- `idx_kyc_customer_id`

---

### 2.6 `beneficiaries`
Stores details of payees added by account holders for transfers.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `beneficiary_id` | `BIGINT` | **PK**, Not Null | Unique beneficiary ID. |
| `account_id` | `VARCHAR(20)` | **FK**, Nullable | Account adding the payee. |
| `beneficiary_name` | `VARCHAR(255)`| Not Null | Payee name. |
| `beneficiary_account_number`| `VARCHAR(50)` | Not Null | Payee account number. |
| `country_id` | `INT` | **FK**, Nullable | Links to `fatf_high_risk_countries`.|
| `created_at` | `TIMESTAMPTZ` | Default: `CURRENT_TIMESTAMP` | Date added. |

**Constraints:**
- `fk_beneficiaries_account`: References `accounts(account_id)`.
- `fk_beneficiaries_country`: References `fatf_high_risk_countries(country_id)`.
- `chk_beneficiaries_no_space`: No spaces in account IDs/numbers.
- `chk_beneficiaries_only_alphabet`: Beneficiary name must be alphabetic/spaces.

**Indexes:** 
- `idx_beneficiaries_account_id`
- `idx_beneficiaries_country_id`

---

### 2.7 `device_logins`
Audit log of devices and IPs used to access the banking application.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `login_id` | `VARCHAR(50)` | **PK**, Not Null | Unique login event ID. |
| `customer_id` | `VARCHAR(20)` | **FK**, Not Null | Links to `customers`. |
| `device_id` | `VARCHAR(255)`| Not Null | Unique device fingerprint. |
| `ip_address` | `VARCHAR(45)` | Not Null | IP Address used. |
| `country_id` | `INT` | **FK**, Nullable | Links to `fatf_high_risk_countries`.|
| `login_time` | `TIMESTAMPTZ` | Default: `CURRENT_TIMESTAMP` | Timestamp of login. |

**Constraints:**
- `fk_device_logins_customer`: References `customers(customer_id)`.
- `fk_device_logins_country`: References `fatf_high_risk_countries(country_id)`.
- `chk_device_login_no_space`: No spaces in customer_id, device_id, ip_address.

**Indexes:** 
- `idx_device_logins_customer_id`
- `idx_device_logins_country_id`
- `idx_device_logins_ip_device`
- `idx_device_logins_time` (DESC)

---

### 2.8 `transactions`
Records all financial movements in and out of accounts.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `txn_id` | `VARCHAR(50)` | **PK**, Not Null | Unique transaction ID. |
| `account_id` | `VARCHAR(20)` | **FK**, Not Null | Source account. |
| `beneficiary_id` | `BIGINT` | **FK**, Nullable | Destination beneficiary. |
| `txn_type` | `VARCHAR(50)` | Not Null | e.g., 'CREDIT', 'DEBIT'. |
| `amount` | `NUMERIC(18,2)`| Not Null | Transaction value. |
| `balance_after_txn`| `NUMERIC(18,2)`| Not Null | Running balance post-txn. |
| `txn_time` | `TIMESTAMPTZ` | Default: `CURRENT_TIMESTAMP` | Timestamp. |
| `channel` | `VARCHAR(50)` | Not Null | e.g., 'WEB', 'MOBILE', 'ATM'. |
| `country_id` | `INT` | **FK**, Nullable | Links to `fatf_high_risk_countries`.|
| `device_id` | `VARCHAR(255)`| Nullable | Device used for txn. |
| `status` | `VARCHAR(20)` | Not Null | e.g., 'SUCCESS', 'FAILED'. |

**Constraints:**
- `fk_txn_account`: References `accounts(account_id)`.
- `fk_txn_beneficiary`: References `beneficiaries(beneficiary_id)`.
- `fk_txn_country`: References `fatf_high_risk_countries(country_id)`.
- `chk_txn_amount`: `amount` >= 0.
- `chk_txn_no_space`: No spaces in `account_id`.

**Indexes:** 
- `idx_transactions_account_id`
- `idx_transactions_beneficiary_id`
- `idx_transactions_country_id`
- `idx_transactions_txn_time` (DESC)
- `idx_transactions_status`
- `idx_transactions_device_id`

---

### 2.9 `aml_alerts`
Generated alerts for suspicious activities based on AML logic.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `alert_id` | `VARCHAR(50)` | **PK**, Not Null | Unique alert ID. |
| `account_id` | `VARCHAR(20)` | **FK**, Not Null | Flagged account. |
| `txn_id` | `VARCHAR(50)` | **FK**, Nullable | Flagged transaction. |
| `alert_type` | `VARCHAR(100)`| Not Null | Type of AML rule broken. |
| `severity` | `VARCHAR(20)` | Not Null | e.g., 'HIGH', 'CRITICAL'. |
| `status` | `VARCHAR(20)` | Default: `'OPEN'` | Alert resolution status. |
| `created_at` | `TIMESTAMPTZ` | Default: `CURRENT_TIMESTAMP` | Time alert was raised. |

**Constraints:**
- `fk_aml_account`: References `accounts(account_id)`.
- `fk_aml_txn`: References `transactions(txn_id)`.

**Indexes:** 
- `idx_aml_alerts_account_id`
- `idx_aml_alerts_txn_id`
- `idx_aml_alerts_status_severity`
- `idx_aml_alerts_created_at` (DESC)

---

### 2.10 `ctr_log`
Currency Transaction Report (CTR) logs for recording large cash movements.

| Column Name | Data Type | Properties | Description |
| :--- | :--- | :--- | :--- |
| `ctr_id` | `VARCHAR(50)` | **PK**, Not Null | Unique CTR log ID. |
| `account_id` | `VARCHAR(20)` | **FK**, Not Null | Account involved. |
| `txn_id` | `VARCHAR(50)` | **FK**, Nullable | Transaction reference. |
| `amount` | `NUMERIC(18,2)`| Not Null | Cash amount. |
| `txn_time` | `TIMESTAMPTZ` | Default: `CURRENT_TIMESTAMP` | Time of transaction. |

**Constraints:**
- `fk_ctr_account`: References `accounts(account_id)`.
- `fk_ctr_txn`: References `transactions(txn_id)`.
- `chk_ctr_amount`: `amount` >= 0.

**Indexes:** 
- `idx_ctr_log_account_id`
- `idx_ctr_log_txn_id`

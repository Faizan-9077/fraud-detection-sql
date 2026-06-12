-- ==============================================================================
-- schema.sql
-- Description: Core table definitions, primary keys, and data types.
-- ==============================================================================

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY, --CIF NUMBER
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    middle_name VARCHAR(50),
    dob DATE NOT NULL,
    pan_number VARCHAR(10) UNIQUE NOT NULL,
    aadhar VARCHAR(12) UNIQUE NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    email VARCHAR(255) UNIQUE,
    risk_rating VARCHAR(20) NOT NULL DEFAULT 'LOW',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE branches (
    branch_id VARCHAR(11) PRIMARY KEY, --IFSC CODE
    branch_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL
);

CREATE TABLE fatf_high_risk_countries (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(50) NOT NULL,
    iso_country_code CHAR(3) UNIQUE NOT NULL,
    risk_level VARCHAR(10) NOT NULL,
    fatf_list_type VARCHAR(10),
    monitoring_status VARCHAR(50) NOT NULL,
    risk_score INT NOT NULL,
    last_updated DATE NOT NULL,
    remark TEXT
);

CREATE TABLE accounts (
    account_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    branch_id VARCHAR(11) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    balance NUMERIC(18, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    last_active_date DATE
);

CREATE TABLE kyc_records (
    kyc_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR(20) NULL,
    status VARCHAR(50) NOT NULL,
    review_date DATE NOT NULL
);

CREATE TABLE beneficiaries (
    beneficiary_id VARCHAR PRIMARY KEY,
    account_id VARCHAR(20) NULL,
    beneficiary_name VARCHAR(255) NOT NULL,
    beneficiary_account_number VARCHAR(50) NOT NULL,
    country_id INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE device_logins (
    login_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    device_id VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    country_id INT,
    login_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    txn_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(20) NOT NULL,
    beneficiary_id VARCHAR(20),
    txn_type VARCHAR(50) NOT NULL,
    amount NUMERIC(18, 2) NOT NULL,
    balance_after_txn NUMERIC(18, 2) NOT NULL,
    txn_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    channel VARCHAR(50) NOT NULL,
    country_id INT,
    device_id VARCHAR(255),
    status VARCHAR(20) NOT NULL,
    fraud_pattern VARCHAR(50) NOT NULL
);

CREATE TABLE aml_alerts (
    alert_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(20) NOT NULL,
    txn_id VARCHAR(50) NULL,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ctr_log (
    ctr_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(20) NOT NULL,
    txn_id VARCHAR(50) NULL,
    amount NUMERIC(18, 2) NOT NULL,
    txn_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
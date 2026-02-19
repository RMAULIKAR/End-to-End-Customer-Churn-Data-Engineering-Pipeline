-- 1. CREATE DATABASE

CREATE DATABASE churn_project;
USE churn_project;




-- 2. CREATE raw_customers table

CREATE TABLE raw_customers (
    customerID VARCHAR(50),
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(10),
    Dependents VARCHAR(10),
    tenure INT,
    PhoneService VARCHAR(10),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20),
    Contract VARCHAR(30),
    PaperlessBilling VARCHAR(10),
    PaymentMethod VARCHAR(50),
    MonthlyCharges DECIMAL(10,2),
    TotalCharges VARCHAR(20),  -- keep as varchar first
    Churn VARCHAR(10)
)




-- 3. Create VIEW cleaned_customer
CREATE OR REPLACE VIEW cleaned_customers AS
SELECT
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    CASE 
        WHEN TRIM(TotalCharges) = '' THEN 0
        ELSE CAST(TotalCharges AS DECIMAL(10,2))
    END AS TotalCharges,
    Churn
FROM raw_customers;





-- 4. CREATE VIEW feature_customers AS
SELECT
    customerID,
    tenure,
    MonthlyCharges,
    TotalCharges,
    SeniorCitizen,

    CASE WHEN gender = 'Male' THEN 1 ELSE 0 END AS gender_male,
    CASE WHEN Partner = 'Yes' THEN 1 ELSE 0 END AS has_partner,
    CASE WHEN Dependents = 'Yes' THEN 1 ELSE 0 END AS has_dependents,
    CASE WHEN PhoneService = 'Yes' THEN 1 ELSE 0 END AS phone_service,
    CASE WHEN PaperlessBilling = 'Yes' THEN 1 ELSE 0 END AS paperless_billing,

    CASE WHEN Contract = 'Month-to-month' THEN 1 ELSE 0 END AS contract_monthly,
    CASE WHEN Contract = 'One year' THEN 1 ELSE 0 END AS contract_one_year,
    CASE WHEN Contract = 'Two year' THEN 1 ELSE 0 END AS contract_two_year,

    CASE 
        WHEN INSTR(LOWER(Churn), 'yes') > 0 THEN 1
        ELSE 0
    END AS churn

FROM cleaned_customers;


-- 5. CREATE TABLE churn_predictions 

CREATE TABLE churn_predictions(
    customerID VARCHAR(50) PRIMARY KEY,
    churn_prediction INT,
    churn_probability FLOAT,
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

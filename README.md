# End-to-End Customer Churn Data Engineering Pipeline

## Overview

An end-to-end layered data pipeline that supports churn model training and incremental batch scoring using MySQL and Python, built from a Data Engineering perspective.

The system implements structured data modeling (raw → cleaned → feature), logical data freshness through SQL views, and separation of training and inference workflows.

---

## Architecture

```
raw_customers (table)
    ↓
cleaned_customers (view)
    ↓
feature_customers (view)
    ↓
Model Training (Python)
    ↓
Saved Model (.pkl)
    ↓
Incremental Batch Inference
    ↓
churn_predictions (table)
```

---

## Key Features

* Layered data architecture (raw → cleaned → feature)
* SQL views for dynamic data freshness
* Logistic Regression with class imbalance handling
* Model persistence using `joblib`
* Incremental, idempotent batch scoring
* Separation of training and inference pipelines

---

## Technology Stack

* Python
* MySQL
* Pandas
* Scikit-learn
* Joblib

---

## How to Run

1. Create database objects using SQL scripts.
2. Run `train_model.py` to train and save the model.
3. Run `predict.py` to execute incremental batch scoring.

---

## Purpose

To demonstrate strong Data Engineering fundamentals, including layered modeling, data lineage awareness, and production-style batch inference design.

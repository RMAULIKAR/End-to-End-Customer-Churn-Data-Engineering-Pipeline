import mysql.connector
import pandas as pd
import joblib

print("Starting prediction script...")

# Connect to DB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PASSWORD", # change this
    database="DB_NAME"  # change this
)

# --------------------------
# Load only NEW customers
# --------------------------

query = """
SELECT f.*
FROM feature_customers f
LEFT JOIN churn_predictions p
ON f.customerID = p.customerID
WHERE p.customerID IS NULL;
"""

df = pd.read_sql(query, conn)

if df.empty:
    print("No new customers to predict.")
    conn.close()
    exit()

print("New customers found:", df.shape[0])

# Save IDs
customer_ids = df["customerID"]

# Prepare feature matrix
X = df.drop(columns=["customerID", "churn"])

# --------------------------
# Load model
# --------------------------

model = joblib.load("models/churn_model.pkl")

# Predict
predictions = model.predict(X)
probabilities = model.predict_proba(X)[:, 1]

# Create results dataframe
results = pd.DataFrame({
    "customerID": customer_ids,
    "churn_prediction": predictions,
    "churn_probability": probabilities
})

# --------------------------
# Insert into DB
# --------------------------

cursor = conn.cursor()

for _, row in results.iterrows():
    cursor.execute("""
        INSERT INTO churn_predictions (customerID, churn_prediction, churn_probability)
        VALUES (%s, %s, %s)
    """, (row["customerID"], int(row["churn_prediction"]), float(row["churn_probability"])))

conn.commit()

print("Predictions inserted successfully!")

conn.close()
print("Database connection closed.")

import mysql.connector

print("Starting connection test...")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PASSWORD",   # change this
    database="DATABASE_NAME" # change this
)

if conn.is_connected():
    print("✅ Connected to MySQL successfully!")
else:
    print("❌ Connection failed")




import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Connecting to database...")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PASSWORD", # change this
    database="DATABASE_NAME"  # change this
)

print("Connected!")

# --------------------------
# Load data
# --------------------------

df = pd.read_sql("SELECT * FROM feature_customers", conn)

print("\nData Loaded Successfully!")
print("Shape of data:", df.shape)

# --------------------------
# Prepare Features & Target
# --------------------------

df = df.drop(columns=["customerID"])

X = df.drop("churn", axis=1)
y = df["churn"]

# --------------------------
# Train-Test Split
# --------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------
# Train Model
# --------------------------

print("\nTraining model...")
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)
print("Model training completed!")

# --------------------------
# Evaluate Model
# --------------------------

y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

conn.close()
print("\nDatabase connection closed.")


import joblib
import os

# create models folder if not exists
os.makedirs("models", exist_ok=True)

# save model
joblib.dump(model, "models/churn_model.pkl")

print("Model saved successfully!")

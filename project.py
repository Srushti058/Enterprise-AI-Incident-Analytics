import mysql.connector
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# =====================================
# MYSQL CONNECTION
# =====================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",   # CHANGE THIS
    database="ai_incident_project"
)

print("MySQL Connected Successfully")

# =====================================
# LOAD DATA FROM MYSQL
# =====================================

query = "SELECT * FROM incidents"

df = pd.read_sql(query, conn)

print("\nDataset Loaded Successfully\n")

print(df.head())

# =====================================
# REMOVE DUPLICATES
# =====================================

df.drop_duplicates(inplace=True)

# =====================================
# CLEAN TEXT COLUMNS
# =====================================

df['severity'] = df['severity'].astype(str).str.strip()

df['priority'] = df['priority'].astype(str).str.strip()

# =====================================
# SEVERITY MAPPING
# =====================================

severity_map = {
    '1 - Minor': 1,
    '2 - Normal': 2,
    '3 - Major': 3,
    '4 - Critical': 4
}

df['severity_score'] = df['severity'].map(severity_map)

# =====================================
# PRIORITY MAPPING
# =====================================

priority_map = {
    '0 - Unassigned': 0,
    '1 - Low': 1,
    '2 - Medium': 2,
    '3 - High': 3
}

df['priority_score'] = df['priority'].map(priority_map)

# =====================================
# HANDLE NaN VALUES
# =====================================

df['severity_score'] = df['severity_score'].fillna(0)

df['priority_score'] = df['priority_score'].fillna(0)

# =====================================
# CONVERT TO INTEGER
# =====================================

df['severity_score'] = df['severity_score'].astype(int)

df['priority_score'] = df['priority_score'].astype(int)

# =====================================
# CREATE RISK SCORE
# =====================================

df['risk_score'] = (
    df['severity_score'] *
    df['max_day']
) + df['priority_score']

print("\nRisk Scores:\n")

print(
    df[
        [
            'severity_score',
            'priority_score',
            'max_day',
            'risk_score'
        ]
    ]
)

# =====================================
# CREATE HIGH RISK LABEL
# =====================================

df['high_risk'] = df['risk_score'].apply(
    lambda x: 1 if x > 10 else 0
)

print("\nHigh Risk Labels:\n")

print(
    df[
        [
            'risk_score',
            'high_risk'
        ]
    ]
)

# =====================================
# FEATURES
# =====================================

X = df[
    [
        'severity_score',
        'priority_score',
        'max_day'
    ]
]

# =====================================
# TARGET
# =====================================

y = df['high_risk']

# =====================================
# SPLIT DATA
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# MACHINE LEARNING MODEL
# =====================================

model = LogisticRegression()

# =====================================
# TRAIN MODEL
# =====================================

model.fit(X_train, y_train)

print("\nModel Training Completed")

# =====================================
# PREDICTIONS
# =====================================

predictions = model.predict(X_test)

print("\nPredictions:\n")

print(predictions)

# =====================================
# ACCURACY
# =====================================

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:\n")

print(accuracy)

# =====================================
# BUSINESS ANALYSIS
# =====================================

print("\nMost Problematic Systems:\n")

print(
    df.groupby('filed_against')['risk_score']
    .mean()
)

print("\nTicket Count By System:\n")

print(
    df['filed_against']
    .value_counts()
)

# =====================================
# SAVE FINAL CSV
# =====================================

df.to_csv("final_incident_analysis.csv", index=False)

print("\nFinal CSV Saved Successfully")
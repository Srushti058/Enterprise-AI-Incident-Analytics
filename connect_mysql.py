import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="ai_incident_project"
)

print("Connected Successfully")

import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="ai_incident_project"
)

query = "SELECT * FROM incidents"

df = pd.read_sql(query, conn)

print(df.head())

print(df.shape)

print(df.columns)

print(df.info())

print(df.isnull().sum())

df.drop_duplicates(inplace=True)

severity_map = {
    '1 - Minor': 1,
    '2 - Normal': 2,
    '3 - Major': 3,
    '4 - Critical': 4
}

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
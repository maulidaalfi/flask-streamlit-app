import streamlit as st
import pandas as pd
import sqlite3 as sql
from sklearn.tree import DecisionTreeClassifier

# Load data from SQLite database
conn = sql.connect('transactions.db')
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

# Display data
st.title("Transaction Data")
st.write(df)

# Feature and target selection
X = df[['amount']]  # Simple example using 'amount' as feature
y = df['status'].apply(lambda x: 1 if x == 'SUCCESS' else 0)  # Encoding target

# Model training
model = DecisionTreeClassifier(max_depth=40, min_samples_leaf=1, min_samples_split=2)
model.fit(X, y)

# Predict function
def predict(amount):
    prediction = model.predict([[amount]])
    return 'SUCCESS' if prediction == 1 else 'FAILED'

# User input
st.header("Predict Transaction Status")
amount = st.number_input("Enter the transaction amount:")
if st.button("Predict"):
    result = predict(amount)
    st.write(f"The predicted transaction status is: {result}")
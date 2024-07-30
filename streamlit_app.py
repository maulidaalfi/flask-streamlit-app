import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import sqlite3

# Fungsi untuk membuat dan menginisialisasi database
def init_db():
    conn = sqlite3.connect('transactions.db')
    conn.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, account_number INTEGER, date TEXT, type TEXT, amount REAL, name TEXT)')
    conn.close()

# Fungsi untuk memasukkan data ke dalam database
def insert_data(account_number, date, type, amount, name):
    conn = sqlite3.connect('transactions.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (account_number, date, type, amount, name) VALUES (?, ?, ?, ?, ?)", (account_number, date, type, amount, name))
    conn.commit()
    conn.close()

# Load dataset
def load_data():
    data = pd.read_csv('transactions.csv')
    return data

# Train model
def train_model(data):
    X = data[['account_number', 'amount']]
    y = data['type']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier(max_depth=40, min_samples_leaf=1, min_samples_split=2)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    return model, accuracy, precision, recall, f1

# Streamlit app
st.title('Transaction Classifier')

st.sidebar.header('User Input Parameters')

def user_input_features():
    account_number = st.sidebar.number_input('Account Number')
    date = st.sidebar.text_input('Date')
    type = st.sidebar.selectbox('Transaction Type', ('FAILED', 'SUCCESS'))
    amount = st.sidebar.number_input('Amount')
    name = st.sidebar.text_input('Name')
    data = {'account_number': account_number, 'date': date, 'type': type, 'amount': amount, 'name': name}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

if st.sidebar.button('Insert Transaction'):
    insert_data(df['account_number'][0], df['date'][0], df['type'][0], df['amount'][0], df['name'][0])
    st.success('Transaction added to database!')

if st.sidebar.button('Train Model'):
    data = load_data()
    model, accuracy, precision, recall, f1 = train_model(data)
    st.write('Model Trained!')
    st.write(f'Accuracy: {accuracy}')
    st.write(f'Precision: {precision}')
    st.write(f'Recall: {recall}')
    st.write(f'F1 Score: {f1}')
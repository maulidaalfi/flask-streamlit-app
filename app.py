from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_transaction():
    return render_template('new_transaction.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            id = request.form['id']
            sender_name = request.form['sender_name']
            sender_upi = request.form['sender_upi']
            receiver_name = request.form['receiver_name']
            receiver_upi = request.form['receiver_upi']
            amount = request.form['amount']
            status = request.form['status']

            with sql.connect("transactions.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO transactions (id, sender_name, sender_upi, receiver_name, receiver_upi, amount, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, sender_name, sender_upi, receiver_name, receiver_upi, amount, status))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("transactions.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM transactions")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

if __name__ == '__main__':
    conn = sql.connect('transactions.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS transactions (id TEXT, sender_name TEXT, sender_upi TEXT, receiver_name TEXT, receiver_upi TEXT, amount REAL, status TEXT)')
    print("Table created successfully")
    conn.close()

    app.run(debug=True)
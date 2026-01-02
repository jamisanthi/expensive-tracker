from flask import Flask, render_template, request, redirect
import sqlite3
import matplotlib.pyplot as plt

app = Flask(__name__)

# ---------- HOME + ADD ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    expense_added = False

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date)
        )
        conn.commit()
        expense_added = True   # 👈 toast trigger

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()

    return render_template(
        'index.html',
        expenses=expenses,
        expense_added=expense_added
    )

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# ---------- GRAPH ----------
@app.route('/graph')
def graph():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    data = cursor.fetchall()
    conn.close()

    categories = [d[0] for d in data]
    amounts = [d[1] for d in data]

    colors = ['#0a1f44', '#16325c', '#1b6ca8', '#144272']

    plt.figure(figsize=(7,4))
    plt.bar(categories, amounts, color=colors[:len(categories)])
    plt.tight_layout()
    plt.savefig('static/expense_graph.png')
    plt.close()

    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True)



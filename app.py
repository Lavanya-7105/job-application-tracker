from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    con = get_db()
    cur = con.cursor()

    # Create table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        apply_date TEXT,
        status TEXT
    )
    """)

    # Fetch all applications
    cur.execute("SELECT * FROM applications")
    data = cur.fetchall()

    # Status summary
    cur.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
    summary = cur.fetchall()

    con.close()
    return render_template("view.html", data=data, summary=summary)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        apply_date = date.today().strftime("%Y-%m-%d")

        if not company or not role:
            return "Company and Role are required"

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO applications (company, role, apply_date, status) VALUES (?, ?, ?, ?)",
            (company, role, apply_date, status)
        )
        con.commit()
        con.close()
        return redirect("/")
    return render_template("add.html")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    new_status = request.form["status"]
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "UPDATE applications SET status=? WHERE id=?",
        (new_status, id)
    )
    con.commit()
    con.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM applications WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

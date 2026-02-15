from flask import Flask, render_template, request, redirect, session

import sqlite3

app = Flask(__name__)
app.secret_key = "washcarsecret"
ADMIN_PASSWORD = "1234"


# 初始化資料庫
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    phone = request.form["phone"]
    date = request.form["date"]
    time = request.form["time"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, phone, date, time) VALUES (?, ?, ?, ?)",
              (name, phone, date, time))
    conn.commit()
    conn.close()

    return "預約成功！<br><a href='/'>回首頁</a>"



@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form["password"]
        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")

    if not session.get("admin"):
        return render_template("login.html")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()

    return render_template("admin.html", bookings=bookings)



if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, render_template, request, redirect, abort
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")

def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg2.connect(DATABASE_URL, sslmode="require")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"].strip()
    phone = request.form["phone"].strip()
    date = request.form["date"].strip()
    time = request.form["time"].strip()

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO bookings (name, phone, booking_date, booking_time) VALUES (%s, %s, %s, %s)",
            (name, phone, date, time)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB ERROR:", e)
        return "Database error", 500

    return redirect("/")


# ✅ 管理頁
@app.route("/admin")
def admin():
    token = request.args.get("token", "")
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        abort(403)

    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM bookings ORDER BY id DESC")
        bookings = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print("ADMIN DB ERROR:", e)
        return "Database error", 500

    return render_template("admin.html", bookings=bookings)



if __name__ == "__main__":
    app.run(debug=True)

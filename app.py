from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "women_safety_secret_key"

DB_NAME = "database.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        incident_type = request.form.get("incident_type", "").strip()
        date = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()

        if not (name and location and incident_type and date and description):
            flash("Please fill in all fields before submitting.", "danger")
            return redirect(url_for("report"))

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO reports (name, location, incident_type, date, description) VALUES (?, ?, ?, ?, ?)",
            (name, location, incident_type, date, description),
        )
        conn.commit()
        conn.close()

        flash("Incident reported successfully. Stay safe!", "success")
        return redirect(url_for("report"))

    return render_template("report.html")


@app.route("/dashboard")
def dashboard():
    conn = get_db_connection()
    reports = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()

    total_reports = len(reports)
    harassment_count = conn.execute(
        "SELECT COUNT(*) FROM reports WHERE incident_type = 'Harassment'"
    ).fetchone()[0]
    theft_count = conn.execute(
        "SELECT COUNT(*) FROM reports WHERE incident_type = 'Theft'"
    ).fetchone()[0]
    other_count = conn.execute(
        "SELECT COUNT(*) FROM reports WHERE incident_type = 'Other'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        reports=reports,
        total_reports=total_reports,
        harassment_count=harassment_count,
        theft_count=theft_count,
        other_count=other_count,
    )


@app.route("/delete/<int:report_id>", methods=["POST"])
def delete_report(report_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()
    flash("Report deleted successfully.", "info")
    return redirect(url_for("dashboard"))


@app.route("/analytics")
def analytics():
    conn = get_db_connection()
    harassment_count = conn.execute(
        "SELECT COUNT(*) FROM reports WHERE incident_type = 'Harassment'"
    ).fetchone()[0]
    theft_count = conn.execute(
        "SELECT COUNT(*) FROM reports WHERE incident_type = 'Theft'"
    ).fetchone()[0]
    stalking_count = conn.execute(
        "SELECT COUNT(*) FROM reports WHERE incident_type = 'Stalking'"
    ).fetchone()[0]
    other_count = conn.execute(
        "SELECT COUNT(*) FROM reports WHERE incident_type = 'Other'"
    ).fetchone()[0]
    conn.close()

    return render_template(
        "analytics.html",
        harassment_count=harassment_count,
        theft_count=theft_count,
        stalking_count=stalking_count,
        other_count=other_count,
    )


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        init_db()
    else:
        init_db()
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import sqlite3
from datetime import datetime

# Load trained model
model = joblib.load("model.pkl")

app = Flask(__name__)

# Create database if it doesn't exist
def init_db():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lot_area REAL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            price_usd REAL,
            price_inr REAL,
            date_time TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        lot_area = float(data["lot_area"])
        bedrooms = int(data["bedrooms"])
        bathrooms = int(data["bathrooms"])

        # Predict price in USD
        price_usd = model.predict(np.array([[lot_area, bedrooms, bathrooms]]))[0]

        # Convert to INR
        conversion_rate = 83
        price_inr = price_usd * conversion_rate

        # Save to database
        conn = sqlite3.connect("predictions.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (lot_area, bedrooms, bathrooms, price_usd, price_inr, date_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (lot_area, bedrooms, bathrooms, float(price_usd), float(price_inr),
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

        return jsonify({
            "price_usd": float(round(price_usd, 2)),
            "price_inr": float(round(price_inr, 2))
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/history")
def history():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, lot_area, bedrooms, bathrooms, price_usd, price_inr, date_time FROM predictions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template("history.html", predictions=rows)

@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/delete_all", methods=["POST"])
def delete_all():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)

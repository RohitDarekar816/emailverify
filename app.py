import os

import jwt
import pymongo
import requests
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from email_verifier import load_disposable_domains, verify_email

app = Flask(__name__)

# JWT key
key = "7020513934"

# mongo connection
client = pymongo.MongoClient(
    "mongodb+srv://myAtlasDBUser:Lifedo4oLsIhay2w@github-webhook.p0pdz5y.mongodb.net/?retryWrites=true&w=majority&appName=Github-Webhook"
)
db = client["emailverify"]
collection = db["users"]


# Load disposable email domains
disposable_domains = load_disposable_domains()

# Allowed file types for CSV uploads
ALLOWED_EXTENSIONS = {"csv"}


# Helper to check if file extension is allowed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# === WEB ROUTES === #


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = db.collection.find_one({"email": email})
        if user:
            return jsonify({"error": "Email is already registered"}), 409

        # For production, hash the password before storing!
        db.collection.insert_one({"email": email, "password": password})
        return jsonify({"success": "Registered successfully"}), 201

    # For GET requests, you might want to return a registration form or a message
    return jsonify({"message": "Send a POST request to register."}), 200


@app.route("/verify", methods=["POST"])
def verify():
    email = request.form.get("email")
    if email:
        result = verify_email(email, disposable_domains)
        return render_template("index.html", result=result)
    return render_template("index.html", error="Please enter a valid email address.")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return render_template("index.html", error="No file part")

    file = request.files["file"]
    if file.filename == "":
        return render_template("index.html", error="No selected file")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join("uploads", filename)
        file.save(filepath)

        results = []
        with open(filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                email = line.strip()
                result = verify_email(email, disposable_domains)
                results.append(result)

        return render_template("index.html", results=results)

    return render_template(
        "index.html", error="Invalid file type. Please upload a CSV."
    )


# === API ROUTES === #


@app.route("/api/verify", methods=["POST"])
def api_verify():
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "Missing 'email' in request body"}), 400

    email = data["email"]
    result = verify_email(email, disposable_domains)
    return jsonify(result)


@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        lines = file.read().decode("utf-8").splitlines()
        results = []

        for line in lines:
            email = line.strip()
            if email:
                result = verify_email(email, disposable_domains)
                results.append(result)

        return jsonify({"results": results})

    return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400


if __name__ == "__main__":
    app.run(debug=True, port=6565, host="0.0.0.0")

from flask import Flask, render_template, request, jsonify
from email_verifier import verify_email, load_disposable_domains
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

disposable_domains = load_disposable_domains()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    email = request.form.get('email')
    if email:
        result = verify_email(email, disposable_domains)
        return render_template('index.html', result=result)
    return render_template('index.html', error="Please enter a valid email address.")

@app.route('/api/verify', methods=['POST'])
def api_verify():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Missing 'email' in request body"}), 400

    result = verify_email(data['email'], disposable_domains)
    return jsonify(result)

# Vercel will use this
def handler(environ, start_response):
    return app(environ, start_response)

from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from email_verifier import verify_email, load_disposable_domains

app = Flask(__name__)

# Load disposable email domains
disposable_domains = load_disposable_domains()

# Allowed file types for CSV uploads
ALLOWED_EXTENSIONS = {'csv'}

# Helper function to check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))

        # Read and process CSV
        results = []
        with open(os.path.join('uploads', filename), 'r') as f:
            lines = f.readlines()
            for line in lines:
                email = line.strip()
                result = verify_email(email, disposable_domains)
                results.append(result)

        return render_template('index.html', results=results)

    return render_template('index.html', error="Invalid file type. Please upload a CSV.")

if __name__ == '__main__':
    app.run(debug=True)

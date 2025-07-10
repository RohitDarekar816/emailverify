# ✉️ Email Verification System

A powerful, developer-friendly web app to verify email addresses for validity, existence, and disposability. Instantly check single emails or upload a CSV for batch verification. Built with Flask, ready for local use or seamless deployment on Vercel.

---

## 🚀 Features

- **Syntax Validation:** Checks if the email address is properly formatted.
- **Disposable Email Detection:** Blocks throwaway emails using a curated list.
- **Domain & MX Record Check:** Ensures the domain exists and can receive emails.
- **SMTP Mailbox Verification:** Optionally checks if the mailbox actually exists (non-intrusive).
- **Batch Verification:** Upload a CSV file to verify multiple emails at once.
- **REST API:** Programmatic access for integration with your own tools.
- **Modern Web UI:** Clean, responsive interface for easy use.

---

## 🖥️ Demo

![Screenshot](static/screenshot.png) <!-- (Add a screenshot if available) -->

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/emailverify.git
cd emailverify
```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed.

```bash
pip install -r requirements.txt
```

### 3. Run the App Locally

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧑‍💻 Usage

### Web Interface

- **Single Email:** Enter an email and click "Verify".
- **Batch:** Upload a CSV file (one email per line) for bulk verification.

### API Endpoints

#### Verify Single Email

```http
POST /api/verify
Content-Type: application/json

{
  "email": "test@example.com"
}
```

**Response:**
```json
{
  "email": "test@example.com",
  "status": "Valid",
  "details": "Mailbox exists (SMTP verified)"
}
```

#### Batch Verification

```http
POST /api/upload
Content-Type: multipart/form-data
file: your_emails.csv
```

**Response:**
```json
{
  "results": [
    { "email": "...", "status": "...", "details": "..." },
    ...
  ]
}
```

---

## ⚙️ Configuration

- **Disposable Domains:** Update `disposable_domains.txt` to maintain your blocklist.
- **SMTP Checks:** The app attempts a non-intrusive SMTP handshake for mailbox existence.

---

## ☁️ Deploy on Vercel

This project is ready for [Vercel](https://vercel.com/) deployment.

1. Push your code to GitHub.
2. Import the repo in Vercel.
3. Vercel auto-detects the Python API via `vercel.json`.

---

## 📂 Project Structure

```
emailverify/
│
├── app.py                  # Main Flask app
├── api/index.py            # Vercel-compatible API entry
├── email_verifier.py       # Email verification logic
├── disposable_domains.txt  # List of disposable email domains
├── requirements.txt        # Python dependencies
├── static/                 # CSS and assets
├── templates/              # HTML templates
└── vercel.json             # Vercel deployment config
```

---

## 🤝 Contributing

Pull requests and issues are welcome!  
Feel free to fork, improve, and share.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

**Happy verifying!** 🚀 
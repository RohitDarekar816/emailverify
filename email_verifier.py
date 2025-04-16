import re
import dns.resolver
from email_validator import validate_email, EmailNotValidError
import smtplib
import socket

# Load known disposable domains from a text file
def load_disposable_domains(file_path='disposable_domains.txt'):
    try:
        with open(file_path, 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def is_valid_syntax(email):
    try:
        valid = validate_email(email)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)

def has_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except:
        return False

def is_disposable(domain, disposable_domains):
    return domain.lower() in disposable_domains

def smtp_check(email, from_email="rohit@cloudtix.in", timeout=10):
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)
    except Exception as e:
        return False, f"MX lookup failed: {e}"

    try:
        server = smtplib.SMTP(timeout=timeout)
        server.connect(mx_record)
        server.helo("example.com")
        server.mail(from_email)
        code, message = server.rcpt(email)
        server.quit()

        if code in [250, 251]:
            return True, "Mailbox exists (SMTP verified)"
        else:
            return False, f"Server rejected RCPT TO: {code} {message.decode()}"
    except (socket.timeout, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, smtplib.SMTPRecipientsRefused) as e:
        return False, f"SMTP connection failed: {e}"
    except Exception as e:
        return False, f"Unhandled SMTP error: {e}"

def verify_email(email, disposable_domains):
    syntax_ok, result = is_valid_syntax(email)
    if not syntax_ok:
        return {"email": email, "status": "Invalid syntax", "details": result}
    
    email = result
    domain = email.split('@')[1]

    if is_disposable(domain, disposable_domains):
        return {"email": email, "status": "Disposable email", "details": "Domain is in disposable list"}

    if not has_mx_record(domain):
        return {"email": email, "status": "Invalid domain", "details": "No MX records found"}

    # New: SMTP mailbox check
    smtp_ok, smtp_msg = smtp_check(email)
    if smtp_ok:
        return {"email": email, "status": "Valid", "details": smtp_msg}
    else:
        return {"email": email, "status": "SMTP Failed", "details": smtp_msg}

# MAIN
if __name__ == "__main__":
    disposable_domains = load_disposable_domains()

    email_input = input("Enter email to verify: ").strip()
    result = verify_email(email_input, disposable_domains)

    print("\n=== Verification Result ===")
    for k, v in result.items():
        print(f"{k}: {v}")

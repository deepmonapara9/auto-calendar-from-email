import imaplib
import email
from email.header import decode_header
import re


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def fetch_unread_emails(email_user, email_pass, limit=3):
    print("📥 Connecting to Gmail IMAP...")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    mail.select("inbox")

    result, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()
    if not email_ids:
        print("📭 No new emails.")
        return []

    latest_email_ids = email_ids[-limit:]  # Get latest unread emails
    emails = []

    print(f"📨 Total unread: {len(email_ids)}. Fetching last {limit}...")

    for num in latest_email_ids:
        result, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_dispo = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_dispo:
                    try:
                        body = part.get_payload(decode=True).decode(
                            "utf-8", errors="ignore")
                        break
                    except:
                        continue
        else:
            body = msg.get_payload(decode=True).decode(
                "utf-8", errors="ignore")

        body = clean_text(body)
        emails.append({
            "subject": subject,
            "body": body
        })

        print("📩 New email fetched:", subject)

    mail.logout()
    return emails

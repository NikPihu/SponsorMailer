import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def send_email(to, subject, body, image_path=None):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach image
    if image_path:
        try:
            with open(image_path, "rb") as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(image_path)}"'
                )
                msg.attach(mime_img)
        except Exception as e:
            print(f"⚠️ Image attach failed: {e}")

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
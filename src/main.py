import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv
import random

from email_sender import send_email
from template_loader import load_templates, get_random_template, personalize_template

load_dotenv()

BATCH_SIZE = 100
PROGRESS_FILE = "progress.txt"

df = pd.read_excel("data/Regn_1623938_BasicInfo_20260326_1115_NoFilters.xlsx")
templates = load_templates()

TOTAL = len(df)

# ✅ Load last progress safely
start_index = 0
if os.path.exists(PROGRESS_FILE):
    try:
        with open(PROGRESS_FILE, "r") as f:
            start_index = int(f.read().strip())
    except:
        start_index = 0

# ✅ Stop if already completed
if start_index >= TOTAL:
    print("All emails already sent.")
    exit()

end_index = min(start_index + BATCH_SIZE, TOTAL)

print(f"\nSending emails from {start_index} to {end_index - 1}")

for idx in range(start_index, end_index):
    row = df.iloc[idx]

    # ✅ Clean name
    name = str(row["Candidate's Name"]).strip()
    if name == "nan":
        name = "Participant"

    # ✅ Clean email
    recipient = str(row["Candidate's Email"]).strip()
    if recipient == "nan" or recipient == "":
        print("⚠️ Skipping empty email")
        continue

    print(f"\n[{idx + 1}/{TOTAL}] Sending to {recipient}...")

    try:
        # Template
        template = get_random_template(templates)

        # Personalize
        email_body = personalize_template(template, company="", hr=name)

        # Send
        send_email(
            to=recipient,
            subject="Solutions 2K26 | Placement Aptitude Test Details",
            body=email_body,
            image_path="assets/Placement_apti_image.png"
        )

        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Sent")

        with open(PROGRESS_FILE, "w") as f:
            f.write(str(idx + 1))

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Failed")
        print(f"Reason: {e}")

    # ✅ Random delay (4–10 sec)
    sleep_time = random.randint(4, 10)
    print(f"Waiting {sleep_time} seconds...")
    time.sleep(sleep_time)

    # ✅ Extra pause every 20 emails
    if (idx - start_index + 1) % 20 == 0:
        print("Taking a longer break (20 sec)...")
        time.sleep(20)

    


print(f"\nBatch completed: {start_index} → {end_index - 1}")
print("Run again to continue next batch.")
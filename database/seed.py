import pymysql
import random
import os
import time

MEDICAL_CENTRES = [
    "Kathmandu Health",
    "Lalitpur Health Centre",
    "Bhaktapur Health Centre",
    "Chitwan Health Centre",
    "Nuwakot Health Centre",
    "Dolakha Health Centre",
    "Rasuwa Health Centre",
    "Sindhuli Health Centre",
    "Makwanpun Health Centre",
    "Ramechhap Health Centre"
]

VISIT_TYPES = [
    "Routine Visit",
    "New Patient",
    "Follow up",
    "Urgent Appointment",
    "Emergency"
]

CHARGE_TYPES = [
    "Cash Payment",
    "Online Payment",
    "Health Insurance",
    "SSF"
]

def seed():
    retries = 10
    for i in range(retries):
        try:
            conn = pymysql.connect(
                host=os.getenv("DB_HOST", "db"),
                port=int(os.getenv("DB_PORT", "3306")),
                db=os.getenv("DB_NAME", "gpclinic"),
                user=os.getenv("DB_USER", "gpclinic_user"),
                password=os.getenv("DB_PASSWORD", "gpclinic_pass"),
            )
            break
        except Exception as e:
            print(f"Waiting for DB... ({i+1}/{retries}): {e}")
            time.sleep(3)
    else:
        raise RuntimeError("Could not connect to the database after retries.")

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM clinic_charges")
    count = cur.fetchone()[0]
    if count >= 500:
        print(f"Database already has {count} rows. Skipping seed.")
        cur.close()
        conn.close()
        return

    rows = []
    for _ in range(500):
        centre = random.choice(MEDICAL_CENTRES)
        visit = random.choice(VISIT_TYPES)
        charge = random.choice(CHARGE_TYPES)
        amount = round(random.uniform(0, 350), 2)
        rows.append((centre, visit, charge, amount))

    cur.executemany(
        "INSERT INTO clinic_charges (medical_centre_name, patient_visit_type, charge_type, amount) VALUES (%s, %s, %s, %s)",
        rows
    )
    conn.commit()
    print(f"Seeded 500 rows successfully.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    seed()

from db_connection import get_db
from models.charges import ClinicChargeCreate, ClinicChargeUpdate


def list_charges(start_row: int, end_row: int, charge_type: str = None, medical_centre_name: str = None):
    limit = end_row - start_row
    offset = start_row
    where_clauses = []
    params = []

    if charge_type:
        where_clauses.append("charge_type = %s")
        params.append(charge_type)
    if medical_centre_name:
        where_clauses.append("LOWER(medical_centre_name) LIKE %s")
        params.append(f"%{medical_centre_name.lower()}%")

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) as total FROM clinic_charges {where_sql}", params)
    total = cur.fetchone()["total"]

    cur.execute(
        f"SELECT * FROM clinic_charges {where_sql} ORDER BY id LIMIT %s OFFSET %s",
        params + [limit, offset],
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"rows": rows, "total": total}


def create_charge(charge: ClinicChargeCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO clinic_charges (medical_centre_name, patient_visit_type, charge_type, amount)
           VALUES (%s, %s, %s, %s)""",
        (charge.medical_centre_name, charge.patient_visit_type, charge.charge_type, charge.amount),
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.execute("SELECT * FROM clinic_charges WHERE id = %s", (new_id,))
    new_row = cur.fetchone()
    cur.close()
    conn.close()
    return new_row


def update_charge(charge_id: int, charge: ClinicChargeUpdate):
    updates = {k: v for k, v in charge.dict().items() if v is not None}
    if not updates:
        return None, "no_fields"

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [charge_id]

    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"UPDATE clinic_charges SET {set_clause} WHERE id = %s", values)
    conn.commit()

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None, "not_found"

    cur.execute("SELECT * FROM clinic_charges WHERE id = %s", (charge_id,))
    updated = cur.fetchone()
    cur.close()
    conn.close()
    return updated, None


def delete_charge(charge_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM clinic_charges WHERE id = %s", (charge_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    cur.close()
    conn.close()
    return deleted


def get_charge_types():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT charge_type FROM clinic_charges ORDER BY charge_type")
    types = [row["charge_type"] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return types


def get_patient_visit_types():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT patient_visit_type FROM clinic_charges ORDER BY patient_visit_type")
    types = [row["patient_visit_type"] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return types
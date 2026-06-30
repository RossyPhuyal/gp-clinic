CREATE TABLE IF NOT EXISTS clinic_charges (
    id SERIAL PRIMARY KEY,
    medical_centre_name VARCHAR(255) NOT NULL,
    patient_visit_type VARCHAR(100) NOT NULL,
    charge_type VARCHAR(100) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);

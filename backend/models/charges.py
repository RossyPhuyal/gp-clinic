from pydantic import BaseModel
from typing import Optional


class ClinicChargeCreate(BaseModel):
    medical_centre_name: str
    patient_visit_type: str
    charge_type: str
    amount: float


class ClinicChargeUpdate(BaseModel):
    medical_centre_name: Optional[str] = None
    patient_visit_type: Optional[str] = None
    charge_type: Optional[str] = None
    amount: Optional[float] = None
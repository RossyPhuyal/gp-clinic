from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.charges import ClinicChargeCreate, ClinicChargeUpdate
from services import charge_service

router = APIRouter(prefix="/api", tags=["charges"])


@router.get("/charges")
def get_charges(
    startRow: int = Query(0, ge=0),
    endRow: int = Query(100, ge=1),
    charge_type: Optional[str] = Query(None),
    medical_centre_name: Optional[str] = Query(None),
):
    try:
        return charge_service.list_charges(startRow, endRow, charge_type, medical_centre_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/charges", status_code=201)
def create_charge(charge: ClinicChargeCreate):
    try:
        return charge_service.create_charge(charge)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/charges/{charge_id}")
def update_charge(charge_id: int, charge: ClinicChargeUpdate):
    try:
        updated, error = charge_service.update_charge(charge_id, charge)
        if error == "no_fields":
            raise HTTPException(status_code=400, detail="No fields to update")
        if error == "not_found":
            raise HTTPException(status_code=404, detail="Record not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/charge-types")
def get_charge_types():
    try:
        return charge_service.get_charge_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient-visit-types")
def get_patient_visit_types():
    try:
        return charge_service.get_patient_visit_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from pydantic import BaseModel, Field
import datetime


class ClinicalDataCreate(BaseModel):
    patient_name: str = Field(..., example="John Doe")
    age: int = Field(..., ge=0, le=120, example=45)
    diagnosis: str = Field(..., example="Hypertension")
    # Added clinical patient data fields
    blood_pressure: str = Field(..., example="120/80")
    heart_rate: int = Field(..., ge=0, example=72)
    medication: str = Field(..., example="Lisinopril")


# The read schema includes the auto-generated fields
class ClinicalDataRead(ClinicalDataCreate):
    id: int
    recorded_at: datetime.datetime

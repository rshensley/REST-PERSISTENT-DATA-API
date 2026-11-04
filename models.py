from sqlalchemy import Column, Integer, String, DateTime
import datetime
from database import Base
from datetime import datetime, timezone


class ClinicalData(Base):
    __tablename__ = "clinical_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)
    # fixed the original example code  to create timzone aware datetime with UTC offset
    recorded_at = Column(
        String, nullable=False, default=lambda: datetime.now(timezone.utc).isoformat()
    )

    # Added clinical patient data fields
    blood_pressure = Column(String, nullable=False)
    heart_rate = Column(Integer, nullable=False)
    medication = Column(String, nullable=False)

    def to_dict(self):
        """Return a JSON-serialisable dict representation."""
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "recorded_at": self.recorded_at,
            # Added clinical patient data fields
            "blood_pressure": self.blood_pressure,
            "heart_rate": self.heart_rate,
            "medication": self.medication,
        }

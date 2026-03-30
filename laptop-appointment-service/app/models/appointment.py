from beanie import Document
from pydantic import Field
from datetime import date, time, datetime
from typing import Optional
import uuid


class Appointment(Document):
    """MongoDB document model for laptop service appointments."""

    appointment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    laptop_id: str

    brand: Optional[str] = None
    model: Optional[str] = None
    issue_type: Optional[str] = None

    appointment_date: date
    appointment_time: time

    service_type: Optional[str] = None
    issue_description: Optional[str] = None

    status: str = "pending"

    class Settings:
        name = "appointments"


class AppointmentHistory(Document):
    """MongoDB document model for tracking appointment status changes."""

    history_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    appointment_id: str
    status: str
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    remarks: Optional[str] = None

    class Settings:
        name = "appointment_history"

from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class AppointmentCreate(BaseModel):
    """Schema for creating a new appointment."""
    customer_id: str
    laptop_id: str
    brand: Optional[str] = None
    model: Optional[str] = None
    issue_type: Optional[str] = None
    appointment_date: date
    appointment_time: time
    service_type: Optional[str] = None
    issue_description: Optional[str] = None


class AppointmentUpdate(BaseModel):
    """Schema for updating appointment details (partial update)."""
    brand: Optional[str] = None
    model: Optional[str] = None
    issue_type: Optional[str] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    service_type: Optional[str] = None
    issue_description: Optional[str] = None


class AppointmentStatusUpdate(BaseModel):
    """Schema for updating only the appointment status."""
    status: str
    remarks: Optional[str] = None


class AppointmentRead(BaseModel):
    """Schema for reading/returning appointment data."""
    appointment_id: str
    customer_id: str
    laptop_id: str
    brand: Optional[str] = None
    model: Optional[str] = None
    issue_type: Optional[str] = None
    appointment_date: date
    appointment_time: time
    service_type: Optional[str] = None
    issue_description: Optional[str] = None
    status: str


class AppointmentHistoryRead(BaseModel):
    """Schema for reading appointment history records."""
    history_id: str
    appointment_id: str
    status: str
    changed_at: datetime
    remarks: Optional[str] = None

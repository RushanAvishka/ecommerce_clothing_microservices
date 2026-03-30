from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
    AppointmentStatusUpdate,
    AppointmentHistoryRead,
)
from app.crud import appointment as crud_appointment

router = APIRouter()


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentCreate):
    result = await crud_appointment.create_appointment(appointment=appointment)
    return result


@router.get("/", response_model=List[AppointmentRead])
async def read_appointments(skip: int = 0, limit: int = 100):
    appointments = await crud_appointment.get_appointments(skip=skip, limit=limit)
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentRead)
async def read_appointment(appointment_id: str):
    appointment = await crud_appointment.get_appointment(appointment_id=appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentRead)
async def update_appointment(appointment_id: str, updates: AppointmentUpdate):
    appointment = await crud_appointment.update_appointment(appointment_id, updates)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/{appointment_id}/status", response_model=AppointmentRead)
async def update_appointment_status(
    appointment_id: str, status_update: AppointmentStatusUpdate
):
    appointment = await crud_appointment.update_appointment_status(
        appointment_id, status_update
    )
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.delete("/{appointment_id}", response_model=AppointmentRead)
async def delete_appointment(appointment_id: str):
    appointment = await crud_appointment.delete_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.get("/{appointment_id}/history", response_model=List[AppointmentHistoryRead])
async def read_appointment_history(appointment_id: str):
    # Verify appointment exists
    appointment = await crud_appointment.get_appointment(appointment_id=appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    history = await crud_appointment.get_appointment_history(appointment_id)
    return history

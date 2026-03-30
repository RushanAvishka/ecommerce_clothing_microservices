from app.models.appointment import Appointment, AppointmentHistory
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentStatusUpdate
from typing import Optional, List


async def get_appointment(appointment_id: str) -> Optional[Appointment]:
    """Retrieve a single appointment by its appointment_id."""
    return await Appointment.find_one(Appointment.appointment_id == appointment_id)


async def get_appointments(skip: int = 0, limit: int = 100) -> List[Appointment]:
    """Retrieve a paginated list of appointments."""
    return await Appointment.find_all().skip(skip).limit(limit).to_list()


async def create_appointment(appointment: AppointmentCreate) -> Appointment:
    """Create a new appointment and add an initial history record."""
    db_appointment = Appointment(**appointment.model_dump())
    await db_appointment.insert()

    # Add initial history record
    history = AppointmentHistory(
        appointment_id=db_appointment.appointment_id,
        status="pending",
        remarks="Appointment Created",
    )
    await history.insert()

    return db_appointment


async def update_appointment(
    appointment_id: str, updates: AppointmentUpdate
) -> Optional[Appointment]:
    """Update appointment details (partial update)."""
    db_appointment = await get_appointment(appointment_id)
    if not db_appointment:
        return None

    update_data = updates.model_dump(exclude_unset=True)
    if update_data:
        await db_appointment.set(update_data)

    return db_appointment


async def update_appointment_status(
    appointment_id: str, status_update: AppointmentStatusUpdate
) -> Optional[Appointment]:
    """Update the appointment status and create a history record."""
    db_appointment = await get_appointment(appointment_id)
    if not db_appointment:
        return None

    await db_appointment.set({Appointment.status: status_update.status})

    # Add history record
    history = AppointmentHistory(
        appointment_id=db_appointment.appointment_id,
        status=status_update.status,
        remarks=status_update.remarks,
    )
    await history.insert()

    return db_appointment


async def delete_appointment(appointment_id: str) -> Optional[Appointment]:
    """Delete an appointment and its associated history records."""
    db_appointment = await get_appointment(appointment_id)
    if not db_appointment:
        return None

    # Delete associated history records
    await AppointmentHistory.find(
        AppointmentHistory.appointment_id == appointment_id
    ).delete()

    await db_appointment.delete()
    return db_appointment


async def get_appointment_history(appointment_id: str) -> List[AppointmentHistory]:
    """Retrieve all history records for a specific appointment."""
    return await AppointmentHistory.find(
        AppointmentHistory.appointment_id == appointment_id
    ).sort("-changed_at").to_list()

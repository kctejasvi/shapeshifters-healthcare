"""
Shapeshifters Healthcare — OPD Appointment Scheduler
Handles booking, cancellation, and slot management for Eesha Hospital.
"""

from datetime import datetime, timedelta
import uuid
from mcp.tools.hospital_data import HOSPITALS, BOOKED_APPOINTMENTS

DAY_ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _resolve_date(date_str: str) -> str:
    """Resolve 'today'/'tomorrow' or return YYYY-MM-DD as-is."""
    s = date_str.strip().lower()
    if s == "today":
        return datetime.now().strftime("%Y-%m-%d")
    if s == "tomorrow":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return datetime.now().strftime("%Y-%m-%d")


def _find_department(hospital: dict, query: str) -> tuple:
    """Find department by code or partial name match. Returns (key, dept_dict)."""
    query_upper = query.strip().upper()
    query_lower = query.strip().lower()
    depts = hospital["departments"]

    # Exact code match
    for key, dept in depts.items():
        if dept["code"] == query_upper:
            return key, dept

    # Partial name match
    for key, dept in depts.items():
        if query_lower in dept["name"].lower() or query_lower in key.lower():
            return key, dept

    return None, None


async def get_departments(args: dict = None) -> dict:
    hospital_id = (args or {}).get("hospital_id", "eesha")
    hospital = HOSPITALS.get(hospital_id)
    if not hospital:
        return {"status": "error", "message": f"Hospital '{hospital_id}' not found."}

    departments = [
        {
            "code":    dept["code"],
            "name":    dept["name"],
            "doctors": len(dept["doctors"]),
        }
        for dept in hospital["departments"].values()
    ]
    return {
        "status":      "success",
        "hospital":    hospital["name"],
        "opd_hours":   hospital["opd_hours"],
        "departments": departments,
    }


async def get_available_slots(args: dict) -> dict:
    hospital_id     = args.get("hospital_id", "eesha")
    department_code = args.get("department_code", "")
    date_str        = args.get("date", "today")

    hospital = HOSPITALS.get(hospital_id)
    if not hospital:
        return {"status": "error", "message": "Hospital not found."}

    dept_key, dept = _find_department(hospital, department_code)
    if not dept:
        return {"status": "error", "message": f"Department '{department_code}' not found."}

    resolved_date = _resolve_date(date_str)
    try:
        date_obj = datetime.strptime(resolved_date, "%Y-%m-%d")
    except ValueError:
        return {"status": "error", "message": "Invalid date format. Use YYYY-MM-DD, 'today', or 'tomorrow'."}

    day_abbr = DAY_ABBR[date_obj.weekday()]

    doctors_slots = []
    for doctor in dept["doctors"]:
        if day_abbr not in doctor["available_days"]:
            continue

        booked = [
            appt["time_slot"]
            for appt in BOOKED_APPOINTMENTS.values()
            if (appt["doctor_id"] == doctor["doctor_id"]
                and appt["date"] == resolved_date
                and appt["status"] == "confirmed")
        ]

        available = [s for s in doctor["slots"] if s not in booked]
        doctors_slots.append({
            "doctor_id":       doctor["doctor_id"],
            "name":            doctor["name"],
            "designation":     doctor["designation"],
            "fee":             doctor["fee"],
            "available_slots": available,
            "booked_slots":    booked,
        })

    if not doctors_slots:
        return {
            "status":  "no_slots",
            "message": f"No doctors available in {dept['name']} on {day_abbr} ({resolved_date}).",
            "date":    resolved_date,
            "day":     day_abbr,
        }

    return {
        "status":     "success",
        "date":       resolved_date,
        "day":        day_abbr,
        "department": dept["name"],
        "dept_code":  dept["code"],
        "doctors":    doctors_slots,
    }


async def book_opd_appointment(args: dict) -> dict:
    hospital_id     = args.get("hospital_id", "eesha")
    department_code = args.get("department_code", "")
    doctor_id       = args.get("doctor_id", "")
    patient_name    = args.get("patient_name", "").strip()
    patient_phone   = args.get("patient_phone", "").strip()
    date_str        = args.get("date", "")
    time_slot       = args.get("time_slot", "").strip()
    reason          = args.get("reason", "").strip()

    if not all([patient_name, patient_phone, date_str, time_slot]):
        return {"status": "error", "message": "Missing required fields: patient_name, patient_phone, date, time_slot."}

    hospital = HOSPITALS.get(hospital_id)
    if not hospital:
        return {"status": "error", "message": "Hospital not found."}

    dept_key, dept = _find_department(hospital, department_code)
    if not dept:
        return {"status": "error", "message": f"Department '{department_code}' not found."}

    # Find the doctor
    doctor = None
    for d in dept["doctors"]:
        if d["doctor_id"] == doctor_id:
            doctor = d
            break
    if not doctor:
        # Fall back to first available doctor
        doctor = dept["doctors"][0] if dept["doctors"] else None
    if not doctor:
        return {"status": "error", "message": "No doctor found."}

    resolved_date = _resolve_date(date_str)
    try:
        date_obj = datetime.strptime(resolved_date, "%Y-%m-%d")
    except ValueError:
        return {"status": "error", "message": "Invalid date."}

    day_abbr = DAY_ABBR[date_obj.weekday()]

    # Check slot availability
    already_booked = any(
        appt["doctor_id"] == doctor["doctor_id"]
        and appt["date"] == resolved_date
        and appt["time_slot"] == time_slot
        and appt["status"] == "confirmed"
        for appt in BOOKED_APPOINTMENTS.values()
    )
    if already_booked:
        return {"status": "error", "message": f"Slot {time_slot} is already booked. Please choose another slot."}

    reference = f"EH-OPD-{uuid.uuid4().hex[:8].upper()}"
    BOOKED_APPOINTMENTS[reference] = {
        "reference":    reference,
        "hospital_id":  hospital_id,
        "hospital":     hospital["name"],
        "department":   dept["name"],
        "dept_code":    dept["code"],
        "doctor_id":    doctor["doctor_id"],
        "doctor":       doctor["name"],
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "date":         resolved_date,
        "day":          day_abbr,
        "time_slot":    time_slot,
        "reason":       reason,
        "fee":          doctor["fee"],
        "status":       "confirmed",
        "booked_at":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Format time with AM/PM
    hour = int(time_slot.split(":")[0])
    minute = time_slot.split(":")[1]
    period = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    time_display = f"{display_hour}:{minute} {period}"

    return {
        "status":       "booked",
        "reference":    reference,
        "hospital":     hospital["name"],
        "department":   dept["name"],
        "doctor":       doctor["name"],
        "patient_name": patient_name,
        "date":         resolved_date,
        "day":          day_abbr,
        "time":         time_display,
        "fee":          doctor["fee"],
        "instructions": [
            "Please arrive 15 minutes before your appointment",
            "Carry all previous medical records and reports",
            "Carry your insurance card if applicable",
            "Fasting not required for OPD consultation",
        ],
        "reminder": "Save your reference number to view or cancel this appointment",
    }


async def cancel_appointment(args: dict) -> dict:
    reference_id  = args.get("reference_id", "").strip().upper()
    patient_phone = args.get("patient_phone", "").strip()

    appt = BOOKED_APPOINTMENTS.get(reference_id)
    if not appt:
        return {"status": "error", "message": f"Appointment '{reference_id}' not found."}

    if appt["patient_phone"] != patient_phone:
        return {"status": "error", "message": "Phone number does not match booking. Cannot cancel."}

    if appt["status"] == "cancelled":
        return {"status": "error", "message": "Appointment is already cancelled."}

    BOOKED_APPOINTMENTS[reference_id]["status"] = "cancelled"
    return {
        "status":    "cancelled",
        "reference": reference_id,
        "message":   f"Appointment {reference_id} has been cancelled successfully.",
    }


async def get_appointment_details(args: dict) -> dict:
    reference_id = args.get("reference_id", "").strip().upper()
    appt = BOOKED_APPOINTMENTS.get(reference_id)
    if not appt:
        return {"status": "error", "message": f"No appointment found with reference '{reference_id}'."}

    return {"status": "success", "appointment": appt}


async def get_todays_appointments(args: dict = None) -> dict:
    hospital_id = (args or {}).get("hospital_id", "eesha")
    today = datetime.now().strftime("%Y-%m-%d")
    todays = [
        appt for appt in BOOKED_APPOINTMENTS.values()
        if appt["date"] == today
        and appt["hospital_id"] == hospital_id
        and appt["status"] == "confirmed"
    ]
    todays.sort(key=lambda x: x["time_slot"])
    return {
        "status": "success",
        "date":   today,
        "count":  len(todays),
        "appointments": todays,
    }

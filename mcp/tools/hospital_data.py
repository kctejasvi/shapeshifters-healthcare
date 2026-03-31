"""
Shapeshifters Healthcare — Hospital Data
Eesha Multispeciality Hospital — OPD + Surgery Data
Scalable: add more hospitals by adding to HOSPITALS dict
"""

from datetime import datetime, timedelta
import uuid

HOSPITALS = {
    "eesha": {
        "hospital_id":   "EESHA001",
        "name":          "Eesha Multispeciality Hospital",
        "short_name":    "Eesha Hospital",
        "address":       "Hyderabad, Telangana",
        "phone":         "+91-XXXXXXXXXX",
        "email":         "appointments@eeshahospital.com",
        "opd_hours":     "9:00 AM – 1:00 PM and 5:00 PM – 8:00 PM",
        "emergency":     "24/7",
        "departments": {
            "general_medicine": {
                "name":     "General Medicine",
                "code":     "GM",
                "doctors": [
                    {
                        "doctor_id":      "DR001",
                        "name":           "Dr. General Physician",
                        "designation":    "Consultant Physician",
                        "available_days": ["Mon","Tue","Wed","Thu","Fri","Sat"],
                        "slots":          ["9:00","9:15","9:30","9:45","10:00",
                                           "10:15","10:30","10:45","11:00","11:15",
                                           "11:30","11:45","12:00","12:15","12:30",
                                           "5:00","5:15","5:30","5:45","6:00"],
                        "fee":            500,
                        "duration_mins":  15,
                    },
                ],
            },
            "surgery": {
                "name": "General Surgery",
                "code": "SG",
                "doctors": [
                    {
                        "doctor_id":      "DR002",
                        "name":           "Dr. General Surgeon",
                        "designation":    "Consultant Surgeon",
                        "available_days": ["Mon","Wed","Fri"],
                        "slots":          ["9:00","9:30","10:00","10:30",
                                           "11:00","11:30","12:00","5:00","5:30"],
                        "fee":            800,
                        "duration_mins":  30,
                    },
                ],
            },
            "cardiology": {
                "name": "Cardiology",
                "code": "CD",
                "doctors": [
                    {
                        "doctor_id":      "DR003",
                        "name":           "Dr. Cardiologist",
                        "designation":    "Consultant Cardiologist",
                        "available_days": ["Tue","Thu","Sat"],
                        "slots":          ["9:00","9:30","10:00","10:30",
                                           "11:00","11:30","5:00","5:30","6:00"],
                        "fee":            1000,
                        "duration_mins":  30,
                    },
                ],
            },
            "orthopaedics": {
                "name": "Orthopaedics",
                "code": "OR",
                "doctors": [
                    {
                        "doctor_id":      "DR004",
                        "name":           "Dr. Orthopaedic Surgeon",
                        "designation":    "Consultant Orthopaedic Surgeon",
                        "available_days": ["Mon","Tue","Thu","Sat"],
                        "slots":          ["9:00","9:30","10:00","10:30",
                                           "11:00","11:30","5:00","5:30"],
                        "fee":            800,
                        "duration_mins":  30,
                    },
                ],
            },
            "gynaecology": {
                "name": "Gynaecology",
                "code": "GY",
                "doctors": [
                    {
                        "doctor_id":      "DR005",
                        "name":           "Dr. Gynaecologist",
                        "designation":    "Consultant Gynaecologist",
                        "available_days": ["Mon","Wed","Fri","Sat"],
                        "slots":          ["9:00","9:30","10:00","10:30",
                                           "11:00","11:30","5:00","5:30","6:00"],
                        "fee":            700,
                        "duration_mins":  30,
                    },
                ],
            },
            "dermatology": {
                "name": "Dermatology",
                "code": "DM",
                "doctors": [
                    {
                        "doctor_id":      "DR006",
                        "name":           "Dr. Dermatologist",
                        "designation":    "Consultant Dermatologist",
                        "available_days": ["Tue","Thu","Sat"],
                        "slots":          ["9:00","9:30","10:00","10:30",
                                           "11:00","5:00","5:30","6:00"],
                        "fee":            600,
                        "duration_mins":  20,
                    },
                ],
            },
            "paediatrics": {
                "name": "Paediatrics",
                "code": "PD",
                "doctors": [
                    {
                        "doctor_id":      "DR007",
                        "name":           "Dr. Paediatrician",
                        "designation":    "Consultant Paediatrician",
                        "available_days": ["Mon","Tue","Wed","Thu","Fri","Sat"],
                        "slots":          ["9:00","9:15","9:30","9:45","10:00",
                                           "10:30","11:00","11:30","5:00","5:30"],
                        "fee":            500,
                        "duration_mins":  15,
                    },
                ],
            },
            "ent": {
                "name": "ENT",
                "code": "EN",
                "doctors": [
                    {
                        "doctor_id":      "DR008",
                        "name":           "Dr. ENT Specialist",
                        "designation":    "Consultant ENT Surgeon",
                        "available_days": ["Mon","Wed","Fri"],
                        "slots":          ["9:00","9:30","10:00","10:30",
                                           "11:00","5:00","5:30"],
                        "fee":            600,
                        "duration_mins":  20,
                    },
                ],
            },
        },
    },
}

# Booked appointments stored in memory
# In production: replace with Supabase/PostgreSQL
BOOKED_APPOINTMENTS = {}

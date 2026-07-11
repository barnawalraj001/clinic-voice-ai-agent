# 🏥 Apollo Clinic Voice AI Receptionist

> A production-style multilingual Voice AI receptionist for Apollo Clinic that autonomously books, reschedules, and cancels appointments using live backend data.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![React](https://img.shields.io/badge/React-Dashboard-61DAFB)
![Retell AI](https://img.shields.io/badge/Retell-Voice_AI-purple)
![Railway](https://img.shields.io/badge/Railway-Deployed-black)

---

# 📌 Overview

This project was developed as part of the **2care.ai Voice AI Engineer Assignment**.

The objective was to build a multilingual AI receptionist capable of handling an end-to-end appointment lifecycle for a real healthcare clinic. The agent interacts naturally with patients over voice, understands both **English and Hindi**, performs real-time appointment management using backend tools, and keeps all appointment data synchronized with a PostgreSQL database.

Unlike a scripted chatbot, the assistant relies entirely on live backend APIs for availability and appointment operations, preventing hallucinated schedules or double bookings.

The React Admin Dashboard is maintained in a separate repository and connects to this backend via REST APIs.

---

## Repository Scope

This repository contains:

- FastAPI backend
- PostgreSQL integration
- Retell AI tool APIs
- Dashboard backend APIs

The React Admin Dashboard is intentionally maintained as a separate repository following a frontend/backend separation similar to production deployments.

---

# ✨ Features

## Voice Agent

- ✅ Natural conversational AI receptionist
- ✅ English + Hindi support
- ✅ Mid-conversation code switching
- ✅ Current date & time awareness
- ✅ Human-like conversation flow
- ✅ Returning patient recognition
- ✅ Live appointment availability lookup
- ✅ Appointment booking
- ✅ Appointment cancellation
- ✅ Appointment rescheduling
- ✅ Cross-branch availability search
- ✅ Dynamic tool calling via Retell AI

---

## Backend

- ✅ FastAPI REST API
- ✅ PostgreSQL database
- ✅ SQLAlchemy ORM
- ✅ Conflict-free appointment booking
- ✅ Double-booking prevention
- ✅ Availability management
- ✅ Dashboard APIs
- ✅ Railway deployment

---

## Admin Dashboard

- ✅ Live statistics
- ✅ Appointment table
- ✅ Doctor directory
- ✅ Patient directory
- ✅ Availability viewer
- ✅ Search & filtering
- ✅ Material UI interface

---

# 🎯 Assignment Requirements Covered

| Requirement | Status |
|------------|--------|
| Book appointment | ✅ |
| Cancel appointment | ✅ |
| Reschedule appointment | ✅ |
| Returning patient | ✅ |
| English | ✅ |
| Hindi | ✅ |
| Code Switching | ✅ |
| Two clinic branches | ✅ |
| Live availability | ✅ |
| PostgreSQL | ✅ |
| Conflict prevention | ✅ |
| Voice AI | ✅ |
| React Dashboard | ✅ |
| Railway Deployment | ✅ |

---


# 🏗️ System Architecture

The solution follows a modular service-oriented architecture where the Voice AI agent, backend services, database, and dashboard are independently connected through REST APIs.

```text

                ┌────────────────────┐
                │     Retell AI      │
                │ Voice Agent (LLM)  │
                └─────────┬──────────┘
                          │
                  Tool Calling (HTTPS)
                          │
                          ▼
              ┌─────────────────────────┐
              │      FastAPI Backend    │
              │                         │
              │ • Availability Service  │
              │ • Booking Service       │
              │ • Patient Service       │
              │ • Dashboard APIs        │
              └─────────┬───────────────┘
                        │
              SQLAlchemy ORM
                        │
                        ▼
             ┌────────────────────┐
             │    PostgreSQL DB   │
             │                    │
             │ Branches           │
             │ Doctors            │
             │ Availability       │
             │ Appointments       │
             └─────────┬──────────┘
                       │
                REST APIs
                       │
                       ▼
          ┌────────────────────────┐
          │ React Admin Dashboard  │
          │ Material UI + Vite      │
          └────────────────────────┘
```

---

# 🛠️ Technology Stack

| Layer | Technology |
|--------|------------|
| Voice Platform | Retell AI |
| Backend | FastAPI |
| Language | Python 3.13 |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Validation | Pydantic |
| Frontend | React + Vite |
| UI Library | Material UI |
| Deployment | Railway |
| Dashboard Hosting | Netlify |

---

# 🎙️ Why Retell AI?

The assignment allowed choosing either **Retell AI** or **Bolna**. I selected **Retell AI** after comparing both platforms against the requirements of a production healthcare receptionist.

### Reasons for choosing Retell AI

- Excellent tool-calling reliability for backend API integrations.
- Low end-to-end conversational latency.
- Built-in telephony support for live phone calls.
- Supports multilingual speech recognition suitable for English and Hindi conversations
- Natural English–Hindi code-switching.
- Robust interruption (barge-in) handling.
- Simple HTTP-based custom function integration with FastAPI.
- Current time awareness for resolving relative dates such as "tomorrow", "next Monday", and "this afternoon".

Retell AI allowed the Voice Agent to remain lightweight while delegating all business logic to backend services, resulting in a clean separation between conversation handling and application logic.

---

# 📂 Repository Structure

This repository contains the backend services for the Apollo Clinic Voice AI system.

```text
voice-ai-backend/

app/
├── models/
├── routers/
├── schemas/
├── services/
├── enums/
├── constants/
├── helpers/

database.py
seed.py
main.py
requirements.txt
README.md
```

The React Admin Dashboard is maintained as a separate repository.

| Repository | Purpose |
|------------|---------|
| Voice AI Backend | FastAPI + PostgreSQL + Retell APIs |
| Admin Dashboard | React + Material UI |

---
# 🗄️ Database Design

The backend uses **PostgreSQL** as the primary datastore. All appointment operations are performed against the database in real time to ensure consistency and prevent double booking.

The database is normalized into four core tables.

---

## Database Schema

### Branches

Stores all clinic locations.

| Column | Description |
|---------|-------------|
| branch_id | Unique branch identifier |
| name | Branch name |
| address | Branch address |

---

### Doctors

Stores doctor information and branch mapping.

| Column | Description |
|---------|-------------|
| doctor_id | Unique doctor ID |
| name | Doctor name |
| specialty | Medical specialty |
| experience_years | Years of experience |
| branch_id | Associated clinic branch |

Relationship

```
Branch
   │
   └──────< Doctor
```

---

### Availability

Represents every appointment slot generated for each doctor.

| Column | Description |
|---------|-------------|
| id | Availability slot ID |
| doctor_id | Doctor |
| date | Appointment date |
| start_time | Slot start time |
| end_time | Slot end time |
| is_booked | Slot status |

Relationship

```
Doctor
   │
   └──────< Availability
```

---

### Appointments

Stores confirmed patient appointments.

| Column | Description |
|---------|-------------|
| appointment_id | Appointment ID |
| patient_name | Patient name |
| phone | Phone number |
| doctor_id | Doctor |
| availability_id | Booked slot |
| status | BOOKED / CANCELLED |
| created_at | Created timestamp |
| updated_at | Updated timestamp |

Relationship

```
Availability
      │
      └────────── Appointment
```

---

# 🔒 Conflict Prevention

The backend enforces appointment consistency at the database level.

Implemented safeguards include:

- One availability slot can only be booked once.
- Double booking is prevented before database commit.
- Cancelled appointments automatically release the associated slot.
- Rescheduling atomically frees the old slot and reserves the new slot.
- Slot availability is always checked against the live database before confirmation.

These checks ensure that the Voice AI agent never confirms appointments using stale or cached information.

---

# 📅 Availability Generation

Rather than manually creating appointment slots, the system generates doctor availability programmatically.

Each doctor receives:

- Working days
- Working hours
- Configurable slot duration
- Automatic slot generation

This approach allows the clinic schedule to scale without manually inserting appointment records.

---

# 🔄 Appointment Lifecycle

The appointment lifecycle follows the workflow below.

```
Patient Request
       │
       ▼
Search Availability
       │
       ▼
Patient Selects Slot
       │
       ▼
Validate Slot
       │
       ▼
Book Appointment
       │
       ▼
Update Availability
       │
       ▼
Store Appointment
```

Cancellation

```
Search Patient
      │
      ▼
Locate Appointment
      │
      ▼
Cancel Appointment
      │
      ▼
Mark Slot Available
```

Rescheduling

```
Search Patient
      │
      ▼
Find New Slot
      │
      ▼
Reserve New Slot
      │
      ▼
Release Old Slot
      │
      ▼
Update Appointment
```

# 🔌 Backend APIs

The FastAPI backend exposes REST APIs that are consumed by both the Voice AI agent and the React Admin Dashboard.

The Voice Agent never performs appointment logic itself. Instead, it calls backend APIs through Retell AI custom functions, ensuring that all scheduling decisions are based on live database state.

---

## Voice Agent APIs

### 1. Search Availability

**POST** `/availability/search`

Searches live appointment availability using optional filters such as specialty, branch, preferred date and preferred time.

Request

```json
{
  "specialty": "Cardiology",
  "branch": "Apollo Multispeciality Hospitals EM Bypass",
  "date": "2026-07-13",
  "preferred_time": "09:00:00"
}
```

Response

```json
{
  "count": 5,
  "available_slots": [
    {
      "availability_id": 29,
      "doctor_name": "Dr Saujatya Chakraborty",
      "specialty": "Cardiology",
      "branch": "Apollo Multispeciality Hospitals EM Bypass",
      "date": "2026-07-13",
      "start_time": "09:00:00",
      "end_time": "09:30:00"
    }
  ]
}
```

---

### 2. Book Appointment

**POST** `/appointments/book`

Books a selected appointment slot after validating that it is still available.

Request

```json
{
  "availability_id": 29,
  "patient_name": "Raj Barnawal",
  "phone": "9988776655"
}
```

Response

```json
{
  "success": true,
  "appointment_id": 15,
  "doctor": "Dr Saujatya Chakraborty",
  "branch": "Apollo Multispeciality Hospitals EM Bypass",
  "date": "2026-07-13",
  "time": "09:00",
  "message": "Appointment booked successfully."
}
```

---

### 3. Search Patient

**POST** `/patients/search`

Looks up a returning patient using their phone number.

Request

```json
{
  "phone": "9988776655"
}
```

Response

```json
{
  "found": true,
  "patient_name": "Raj Barnawal",
  "appointment_count": 2,
  "last_appointment": {
    "doctor": "Dr Saujatya Chakraborty",
    "specialty": "Cardiology",
    "branch": "Apollo Multispeciality Hospitals EM Bypass",
    "date": "2026-07-13",
    "time": "09:00"
  }
}
```

---

### 4. Cancel Appointment

**PUT** `/appointments/cancel`

Cancels an existing appointment and releases the booked availability slot.

---

### 5. Reschedule Appointment

**PUT** `/appointments/reschedule`

Moves an appointment to a new availability slot while atomically updating slot availability.

---

# 📊 Dashboard APIs

The React Admin Dashboard consumes the following APIs.

| Endpoint | Purpose |
|----------|---------|
| GET `/dashboard/stats` | Dashboard summary |
| GET `/dashboard/appointments` | Appointment table |
| GET `/dashboard/availability` | Availability table |
| GET `/dashboard/doctors` | Doctors table |
| GET `/dashboard/patients` | Patient table |

---

# 🎙️ Voice Agent Tool Calling

The Voice AI agent communicates with the backend exclusively through custom function calls.

Implemented tools include:

- **search_availability**
- **book_appointment**
- **search_patient**
- **cancel_appointment**
- **reschedule_appointment**

The agent never fabricates appointment information. Every booking decision is based on live API responses.

---

# 🤖 Conversation Flow

## New Patient

```text
Patient
   │
   ▼
Search Availability
   │
   ▼
Select Appointment
   │
   ▼
Collect Name
   │
   ▼
Collect Phone Number
   │
   ▼
Book Appointment
   │
   ▼
Confirmation
```

---

## Returning Patient

```text
Patient
   │
   ▼
Search Patient
   │
   ▼
Retrieve Previous Appointment
   │
   ▼
Offer Same Doctor
   │
   ▼
Search Availability
   │
   ▼
Book Appointment
```

---

## Cancellation

```text
Patient
   │
   ▼
Search Patient
   │
   ▼
Read Appointment Details
   │
   ▼
User Confirms
   │
   ▼
Cancel Appointment
   │
   ▼
Confirmation
```

---

## Rescheduling

```text
Patient
   │
   ▼
Search Patient
   │
   ▼
Search New Availability
   │
   ▼
Patient Selects Slot
   │
   ▼
Reschedule Appointment
   │
   ▼
Confirmation
```


# 🧪 Evaluation & Testing

The project was tested using both the Retell AI Chat Simulator and live voice simulation to validate the complete appointment workflow.

The evaluation focused on real conversational scenarios rather than isolated API testing.

---

# ✅ Scenarios Tested

The following scenarios were successfully tested.

| Scenario | Status |
|-----------|--------|
| New patient appointment booking | ✅ |
| Returning patient recognition | ✅ |
| Live availability search | ✅ |
| Appointment cancellation | ✅ |
| Appointment rescheduling | ✅ |
| English conversation | ✅ |
| Hindi conversation | ✅ |
| English-Hindi code switching | ✅ |
| Cross-branch availability search | ✅ |
| Conflict / double-booking prevention | ✅ |
| Dashboard synchronization | ✅ |

---

# Voice Conversation Examples

Examples of successful conversations include:

- Booking the earliest available cardiology appointment.
- Returning patient booking with the same doctor.
- Cancelling an existing appointment.
- Rescheduling to another available slot.
- Switching between English and Hindi naturally during the same conversation.
- Asking for alternate dates and times.
- Cross-branch availability lookup.

---

# Measured Latency

Retell AI provides latency measurements for each response during testing.

Typical observed values were:

| Component | Approximate Latency |
|-----------|--------------------:|
| Automatic Speech Recognition (ASR) | 150–350 ms |
| LLM Processing | 900–1400 ms |
| Backend Tool Call | 100–300 ms |
| Text-to-Speech (TTS) | 150–300 ms |
| Overall Response | ~1.3–2.0 s |

The total response time remained suitable for natural phone conversations.

---

# Backend Performance

Backend APIs were tested using Swagger UI and Retell AI custom functions.

The backend performs:

- Live availability lookup
- Appointment validation
- Conflict detection
- PostgreSQL writes
- Slot updates

Average API response time remained well below one second during testing.

---

# Conflict Prevention

The booking workflow was tested against multiple booking attempts for the same availability slot.

Verified behavior:

- Only one appointment can occupy a slot.
- Duplicate bookings are rejected.
- Cancelled appointments release their availability.
- Rescheduling frees the previous slot and reserves the new slot atomically.

This ensures consistency even when multiple booking attempts occur.

---

# Admin Dashboard Verification

The React dashboard was used to verify backend operations in real time.

Verified items include:

- Appointment creation
- Appointment cancellation
- Appointment rescheduling
- Patient history
- Doctor information
- Availability updates

This provided an additional verification layer beyond API testing.

---

# Design Decisions

Several design decisions were made to improve conversation quality and reliability.

- Business logic resides entirely in the backend.
- The Voice Agent only orchestrates conversations.
- Live availability is always fetched before offering appointments.
- Returning patients are identified using their phone number.
- Internal identifiers such as availability IDs are never exposed to patients.
- The agent asks only for missing information and avoids redundant questions.

---

# Assignment Coverage

| Requirement | Implemented |
|-------------|-------------|
| End-to-end appointment lifecycle | ✅ |
| Live PostgreSQL datastore | ✅ |
| Double-booking prevention | ✅ |
| Multilingual conversation | ✅ |
| English-Hindi code switching | ✅ |
| Returning patient recognition | ✅ |
| Cross-branch search | ✅ |
| React Admin Dashboard | ✅ |
| Railway deployment | ✅ |
| Retell AI telephony | ✅ |

---

# Known Limitations

The following items were intentionally left outside the current implementation scope.

- Cliniko PMS integration was not implemented. The project uses a custom PostgreSQL-backed scheduling system.
- Callback recovery after dropped calls is not yet supported.
- SMS/WhatsApp appointment reminders are not included.
- Authentication for the admin dashboard is not implemented.
- Dashboard updates require a manual refresh instead of real-time WebSocket synchronization.

These limitations were considered non-critical for the assignment and can be added incrementally.

---

# Future Improvements

Potential production enhancements include:

- Cliniko or other PMS integration.
- WebSocket-based live dashboard updates.
- Calendar synchronization (Google Calendar / Outlook).
- SMS and WhatsApp reminders.
- Email confirmations.
- Authentication and role-based access control.
- Docker and Kubernetes deployment.
- Appointment reminder automation.
- Analytics dashboard for clinic operations.

---


# 🚀 Deployment

| Component | Platform |
|-----------|----------|
| Voice Agent | Retell AI |
| Backend API | Railway |
| PostgreSQL | Railway |
| Admin Dashboard | Netlify (Separate Repository) |

---

# ⚙️ Local Setup

## Backend

```bash
git clone https://github.com/barnawalraj001/clinic-voice-ai-agent

cd clinic-voice-ai-agent

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Frontend

The React Admin Dashboard is available in a separate repository.

```bash
git clone https://github.com/barnawalraj001/PMS-dashboard-for-voice-ai

cd PMS-dashboard-for-voice-ai

npm install

npm run dev
```

Dashboard

```
http://localhost:5173
```

---

# 📞 Live Demo

## Live Backend

```
https://web-production-81570.up.railway.app/  
```

---

## Swagger

```
https://web-production-81570.up.railway.app/docs
```

---

## Admin Dashboard

```
https://pms-dashboard-for-voice-ai.netlify.app/
```

*(Hosted from a separate frontend repository.)*



# 👨‍💻 Author

**Raj Barnawal**

AI Engineer

GitHub

```
https://github.com/barnawalraj001 
```

LinkedIn

```
https://linkedin.com/in/barnawalraj001
```

---

# 🙏 Acknowledgements

This project was developed as part of the **2care.ai Voice AI Engineer Assignment**.

The goal of the assignment was to design and build a production-style multilingual healthcare Voice AI receptionist capable of handling real appointment workflows through live backend integrations.

The implementation emphasizes modular backend architecture, reliable tool calling, real-time database consistency, and a conversational experience that closely resembles a human clinic receptionist.
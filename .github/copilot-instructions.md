# TibaCare Hospital Management System - AI Agent Instructions

## Project Overview
TibaCare is a full-stack hospital management system with role-based authentication (Patients and Doctors). The system manages departments, doctor profiles, appointments, and medical records.

**Architecture:** React frontend (port 4000) + Flask backend (port 5555) with SQLite database

## Core Components

### Backend (Flask) - `/server/`
- **Models** (`models.py`): Four main entities with SQLAlchemy + serializer mixins
  - `Patient`: first_name, last_name, email (unique), age, gender, phone_number, password (bcrypt hashed)
  - `Doctor`: first_name, last_name, email (unique), title, doctorId, specialty, bio, education, certifications, image (filename), department_id, password
  - `Department`: name, description, image (filename), one-to-many doctors
  - `Appointment`: time, date, medical_records, patient_id FK, doctor_id FK

- **Key Patterns:**
  - Custom `to_dict()` methods on models (override SerializerMixin defaults) - see `Doctor.to_card_dict()` and `Doctor.to_profile_dict()` variants
  - Circular relationship handling via `serialize_rules` to prevent infinite recursion
  - BCrypt password hashing used consistently in signup/login endpoints

- **API Routes** (Flask-RESTful resources in `app.py`):
  - Auth: `/api/doctorsignup`, `/api/doctorlogin`, `/api/patientsignup`, `/api/patientlogin`, `/api/check_session`, `/api/logout`
  - Data: `/api/departments`, `/api/departments/<id>` (doctors by dept), `/api/doctor/<id>`, `/api/patient/<id>`, `/api/doctors/<id>` (profile), `/api/appointments`
  - Images: `/api/images?model=doctor&filename=<name>` (fetch stored images from `server/images/`)
  - Session-based auth: user_id and user_role stored in Flask session with secure cookies

### Frontend (React) - `/client/src/`
- **Auth Flow:** `AuthContext.js` + `PrivateRoute.js`
  - Context manages global `user`, `role`, `loading` state
  - `useAuth()` hook provides access across components
  - Session check on app load via `/api/check_session`
  - `PrivateRoute` redirects unauthenticated users to `/login`

- **Component Structure:**
  - `App.js`: Main wrapper with AuthProvider, imports Navbar/Footer/Gallery
  - `Routes.js`: Central route definitions (16 routes total, mix of public + protected)
  - **Protected Routes:** `/patientdashboard`, `/doctordashboard` (both use PrivateRoute)
  - **Public Routes:** `/`, `/login`, `/signup`, `/departments`, `/departments/:id`, `/doctors/:id`, `/about`, `/contact`

- **Key Components:**
  - `Login.js` / `DoctorLogin.js`: Handle separate auth flows (form validation via Formik + Yup)
  - `BookAppointment.js`: Patient appointment creation
  - `DoctorDashboard.js` / `PatientDashboard.js`: Role-specific views
  - `DoctorProfile.js` / `DoctorProfileContainer.js`: Doctor info display

- **Styling:** CSS modules per component + Tailwind (dev dependency in package.json)
- **API Base:** Proxied to `http://127.0.0.1:5555` in package.json

## Development Workflows

### Starting Development
```bash
# Backend: Install dependencies and seed DB
cd server
pipenv install
pipenv shell
python seed.py  # Initializes 16 departments + 50+ seeded doctors/patients
python app.py   # Runs on port 5555

# Frontend: Install and start dev server
cd client
npm install
npm start       # Runs on port 4000 (set via PORT=4000 env var)
```

### Testing
- **React Tests:** `npm test` in `/client/` (uses jest + react-testing-library, basic setup in `testing/`)
- **Existing Tests:** `/client/src/testing/App.test.js` (minimal coverage)
- **No backend tests yet** - add via pytest if needed

### Database
- **Location:** `server/instance/app.db` (SQLite)
- **Migrations:** Alembic setup in `server/migrations/` - use `flask db migrate/upgrade` after model changes
- **Seeding:** `server/seed.py` creates departments from hardcoded list, generates 50+ fake doctors with images

## Project-Specific Conventions

### API Response Format
```javascript
// Success (200)
{ "message": "Login successful", "data": {...user}, "status": 200 }

// Auth error (401)
{ "error": "Invalid credentials" }

// Server error (500)
{ "error": str(exception) }
```

### Image Handling
- Doctors/Departments store `image` field as filename only (e.g., "Dr1.jpg", "cardiology.jpg")
- Frontend fetches via: `GET /api/images?model=doctor&filename=Dr1.jpg`
- Backend serves from `server/images/` using `send_from_directory()`
- Doctor signup accepts multipart form with file upload, uses `secure_filename()`

### Session Management
- Flask sessions use secure cookies (SESSION_COOKIE_SECURE=True in prod)
- Frontend sends requests with `credentials: 'include'` to include session cookies
- CORS configured for localhost:4000 origin only

### Form Validation
- Patient/Doctor signup use **Formik + Yup** (see `client/src/components/Signup.js`, `PatientLogin.js`)
- Server-side validation on duplicate emails (unique=True constraints)

## Integration Points

### Cross-Component Communication
1. **Authentication:** AuthContext (App wrapper) → all components via useAuth()
2. **Routing:** Routes.js centralizes all page routing definitions
3. **Appointments:** Patients book via PatientDashboard → API creates Appointment record linking patient_id + doctor_id

### Database Relationships
```
Department (1) ← (many) Doctor
Patient (1) ← (many) Appointment (many) → (1) Doctor
```

### Frontend-Backend Contract
- All doctor endpoints return different shapes: `to_dict()` (full), `to_card_dict()` (minimal for cards), `to_profile_dict()` (public profile)
- Department detail includes nested doctor list via `doctors: [doctor.to_dict() for ...]`

## Common Tasks

### Adding a New Feature
1. **Model Changes:** Update `server/models.py` + add migration `flask db migrate`
2. **Backend Endpoint:** Add resource class to `server/app.py` + `api.add_resource()`
3. **Frontend:** Create component in `client/src/components/`, add route to `Routes.js`, integrate with AuthContext if protected
4. **Testing:** Add to `client/src/testing/` for React, pytest for Flask if added

### Debugging
- **Backend errors:** Check `server/` terminal for Flask stack traces (Flask-RESTful formats responses)
- **Frontend errors:** React DevTools + Network tab for API calls (check CORS if blocked)
- **Session issues:** Verify credentials:include + SESSION_COOKIE_SECURE setting

### Database Resets
- Drop all + recreate: `python seed.py` (destructive but reproducible)
- Backup before destructive operations: SQLite db located at `server/instance/app.db`

## Key Files Reference
- **Entry Points:** `client/src/index.js`, `server/app.py`
- **Core Logic:** `client/src/components/AuthContext.js` (auth state), `server/models.py` (data schema)
- **Routes Definition:** `client/src/components/Routes.js` (frontend), `server/app.py` (backend APIs)
- **Database:** `server/instance/app.db`, `server/seed.py` (initialization)

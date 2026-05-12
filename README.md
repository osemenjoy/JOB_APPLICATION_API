# Job Application API

A professional REST API for managing job applications built with **FastAPI**, featuring **user authentication**, **database persistence**, and **advanced filtering**.

## ✨ Features

### Authentication & User Management
- ✅ User registration with password validation
- ✅ JWT-based authentication (access & refresh tokens)
- ✅ Token refresh for seamless session management
- ✅ User logout with token revocation
- ✅ Role-based access control (Admin & Regular Users)

### Job Application Management
- ✅ Submit job applications with cover letter and resume
- ✅ Retrieve applications with pagination
- ✅ Update application status (admin only)
- ✅ Delete applications
- ✅ Skill-based filtering for applicants and hirers
- ✅ Application status tracking (pending, reviewed, shortlisted, rejected, accepted)
- ✅ Company profile management for hirers
- ✅ Applicant profile with skills and experience

### Database & Data Persistence
- ✅ SQLAlchemy ORM integration
- ✅ Support for SQLite (default) and PostgreSQL
- ✅ User and Application models with relationships
- ✅ Refresh token management
- ✅ Database initialization on startup

### API Features
- ✅ Interactive Swagger UI documentation
- ✅ ReDoc alternative documentation
- ✅ CORS support for frontend integration
- ✅ Comprehensive error handling
- ✅ Input validation with Pydantic schemas
- ✅ Automatic database migrations support

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.104+
- **Web Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt with passlib
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Validation**: Pydantic v2
- **Email Validation**: email-validator

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### Option 1: Automatic Setup (Windows)

```bash
# Navigate to project directory
cd JOB_APP_API

# Run setup script
setup.bat
```

### Option 2: Manual Setup

#### 1. Create Virtual Environment
```bash
python -m venv venv
```

#### 2. Activate Virtual Environment

**Windows:**
```powershell
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment (Optional)
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# By default, SQLite database is used (no configuration needed)
```

### Option 3: Start with Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## ▶️ Running the API

### Start the Server

**Using setup script:**
```bash
run.bat
```

**Directly with Python:**
```bash
python main.py
```

**Using Uvicorn directly:**
```bash
uvicorn main:app --reload
```

**With custom host and port:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

## 📚 API Documentation

### Interactive API Explorer
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

### User Registration

**Endpoint:** `POST /auth/register`

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "full_name": "John Doe",
    "password": "SecurePass123",
    "role": "APPLICANT"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "APPLICANT",
  "is_active": true,
  "created_at": "2024-11-15T10:30:45.123456",
  "updated_at": "2024-11-15T10:30:45.123456"
}
```

**Supported Roles:**
- `APPLICANT`: Job seeker
- `HIRER`: Company hiring manager

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one digit

### User Login

**Endpoint:** `POST /auth/login`

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Using Access Token

Include the token in the `Authorization` header:

```bash
curl -X GET "http://localhost:8000/applications" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Refresh Access Token

**Endpoint:** `POST /auth/refresh`

```bash
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### Logout

**Endpoint:** `POST /auth/logout`

```bash
curl -X POST "http://localhost:8000/auth/logout" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📝 Job Application Endpoints

### Submit Application

**Endpoint:** `POST /applications`

**Request Body:**
```json
{
  "job_id": 1,
  "cover_letter": "I am interested in this position...",
  "resume_url": "https://example.com/resume.pdf"
}
```

```bash
curl -X POST "http://localhost:8000/applications" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 1,
    "cover_letter": "I am very interested in this position...",
    "resume_url": "https://example.com/resume.pdf"
  }'
```

**Response:**
```json
{
  "id": 1,
  "applicant_id": 1,
  "job_id": 1,
  "company_id": 1,
  "cover_letter": "I am very interested...",
  "resume_url": "https://example.com/resume.pdf",
  "status": "PENDING",
  "applied_at": "2024-11-15T10:30:45.123456",
  "updated_at": "2024-11-15T10:30:45.123456"
}
```

**Error Handling:**
- Returns 400 if applicant has already applied to the job
- Returns 404 if job not found
- Returns 403 if user is not an applicant

### Get My Applications

**Endpoint:** `GET /applications`

```bash
curl -X GET "http://localhost:8000/applications?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Query Parameters:**
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=10, max=100): Records per page

### Get Specific Application

**Endpoint:** `GET /applications/{application_id}`

```bash
curl -X GET "http://localhost:8000/applications/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Access Rules:**
- Users can only access their own applications
- Admins can access any application

### Update Application

**Endpoint:** `PUT /applications/{application_id}`

```bash
curl -X PUT "http://localhost:8000/applications/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "REVIEWED"
  }'
```

**Note:** Only admins can update application status

### Delete Application

**Endpoint:** `DELETE /applications/{application_id}`

```bash
curl -X DELETE "http://localhost:8000/applications/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Filter by Skill

**Endpoint:** `GET /applications/filter/skill`

```bash
curl -X GET "http://localhost:8000/applications/filter/skill?skill=Python&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Role-Based Behavior:**
- **Applicants**: Returns jobs they applied to that require the searched skill
- **Hirers**: Returns applications from their company where applicants have the searched skill

**Query Parameters:**
- `skill` (string, required): Skill to filter by (case-insensitive)
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=10, max=100): Records per page

## � Role-Based Features

### Applicant Features
- Create and manage applicant profile with skills and experience
- Browse and apply for jobs
- View their own applications
- Filter their applications by job skill requirements
- Upload and manage resumes
- Track application status

### Hirer (Company) Features
- Create and manage company profile
- Post job listings with required skills
- View all applications to their jobs
- Filter applicants by specific skills
- Update application status (reviewed, shortlisted, rejected, accepted)
- Manage job postings

### Admin Features
- Access all users and applications
- Update application statuses
- Manage user accounts
- View system-wide statistics

## 📊 Database Models

### User Model
```python
- id: Integer (Primary Key)
- email: String (Unique, Email)
- full_name: String
- hashed_password: String
- role: Enum (APPLICANT, HIRER)
- is_active: Boolean
- verification_code: String (Optional)
- verification_code_expires_at: DateTime (Optional)
- created_at: DateTime
- updated_at: DateTime
- applicant_profile: Relationship to ApplicantProfile (Optional)
- company_profile: Relationship to CompanyProfile (Optional)
- refresh_tokens: Relationship to RefreshToken
```

## 🧪 Testing

### Run Tests

```bash
# Make sure the API server is running
python main.py

# In another terminal, run the test suite
pytest app/tests/ -v
```

### Manual Testing with Swagger UI

1. Navigate to http://localhost:8000/docs
2. Register a new user using `/auth/register` endpoint
3. Login using `/auth/login` endpoint
4. Copy the `access_token` from the response
5. Click the "Authorize" button at the top and enter: `Bearer YOUR_ACCESS_TOKEN`
6. Test all endpoints with the interactive Swagger UI

### Key Test Scenarios

- User registration with different roles (APPLICANT, HIRER)
- User login and token management
- Job creation and management (for hirers)
- Job application submission
- Duplicate application prevention
- Skill-based filtering for applicants
- Skill-based filtering for hirers
- Application status updates (admin only)
- Access control and authorization

## 🗄️ Database Configuration

### SQLite (Default - Development)

```env
DATABASE_URL=sqlite:///./job_applications.db
```

Database file will be created automatically in the project directory.


## 📁 Project Structure

```
JOB_APP_API/
├── main.py                              # FastAPI application entry point
├── alembic.ini                          # Database migration config
├── requirements.txt                     # Python dependencies
├── README.md                            # This file
├── alembic/                             # Database migrations
│   ├── versions/                        # Migration scripts
│   ├── env.py                          # Alembic environment configuration
│   └── script.py.mako                  # Migration template
├── app/
│   ├── __init__.py
│   ├── main.py                         # App initialization and configuration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                     # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py                  # API router setup
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py             # Authentication endpoints
│   │           ├── applications.py     # Application endpoints
│   │           ├── jobs.py             # Job endpoints
│   │           └── users.py            # User endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                   # Configuration settings
│   │   ├── security.py                 # Authentication and security
│   │   └── settings.py                 # Environment settings
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                     # SQLAlchemy declarative base
│   │   └── session.py                  # Database session management
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── logging.py                  # Logging middleware
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                     # User, ApplicantProfile, CompanyProfile models
│   │   ├── application.py              # Application model
│   │   └── job.py                      # Job model
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── application_repository.py   # Application data access
│   │   ├── job_repository.py           # Job data access
│   │   └── user_repository.py          # User data access
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── application.py              # Application validation schemas
│   │   ├── job.py                      # Job validation schemas
│   │   ├── token.py                    # Token schemas
│   │   └── user.py                     # User validation schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── application_service.py      # Application business logic
│   │   ├── job_service.py              # Job business logic
│   │   └── user_service.py             # User business logic
│   └── tests/
│       ├── __init__.py
│       └── applications.py             # Application tests
```

## 🔒 Security Best Practices

1. **Change Secret Key**: Update `SECRET_KEY` in `.env` for production
   ```bash
   # Generate a secure key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Use HTTPS**: Enable SSL/TLS in production

3. **Environment Variables**: Never commit `.env` file to version control

4. **Token Expiration**: Access tokens expire in 30 minutes, refresh tokens in 7 days

5. **Password Hashing**: All passwords are hashed using bcrypt

6. **CORS Configuration**: Update `CORS_ORIGINS` in `config.py` for your domain

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

---

**Created:** November 2024  
**Version:** 2.0.0 (with authentication & database)

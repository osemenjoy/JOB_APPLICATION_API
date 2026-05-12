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
- ✅ Submit job applications with detailed information
- ✅ Retrieve applications with pagination
- ✅ Update application details and status
- ✅ Delete applications
- ✅ Comprehensive filtering and search capabilities
- ✅ Application status tracking (pending, reviewing, accepted, rejected)
- ✅ Application rating system (for admins)

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
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-11-15T10:30:45.123456",
  "updated_at": "2024-11-15T10:30:45.123456"
}
```

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
    "username": "john_doe",
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

```bash
curl -X POST "http://localhost:8000/applications" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "555-987-6543",
    "skills": ["JavaScript", "React", "Node.js"],
    "experience_years": 5,
    "position": "Frontend Developer",
    "cover_letter": "I am interested in this position..."
  }'
```

### Get All Applications

**Endpoint:** `GET /applications`

```bash
curl -X GET "http://localhost:8000/applications?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Query Parameters:**
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=10, max=100): Records per page

### Get Specific Application

**Endpoint:** `GET /applications/{id}`

```bash
curl -X GET "http://localhost:8000/applications/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Application

**Endpoint:** `PUT /applications/{id}`

```bash
curl -X PUT "http://localhost:8000/applications/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "experience_years": 6,
    "skills": ["JavaScript", "React", "Node.js", "TypeScript"]
  }'
```

**Admin-only fields (requires admin role):**
- `status`: pending, reviewing, accepted, rejected
- `rating`: 0-5
- `notes`: Internal notes

### Delete Application

**Endpoint:** `DELETE /applications/{id}`

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

### Advanced Search & Filter

**Endpoint:** `GET /applications/filter/search`

```bash
curl -X GET "http://localhost:8000/applications/filter/search?skill=Python&position=Backend&min_experience=3&max_experience=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Available Filters:**
- `skill`: Exact skill name (case-insensitive)
- `position`: Position name (partial match)
- `min_experience`: Minimum years of experience
- `max_experience`: Maximum years of experience
- `status`: Application status (pending, reviewing, accepted, rejected)
- `min_rating`: Minimum rating (admin only)
- `skip`: Pagination offset
- `limit`: Pagination limit

## 👨‍💼 Admin Endpoints

### Get All Users (Admin Only)

**Endpoint:** `GET /admin/users`

```bash
curl -X GET "http://localhost:8000/admin/users?skip=0&limit=10" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### Get All Applications (Admin Only)

**Endpoint:** `GET /admin/applications`

```bash
curl -X GET "http://localhost:8000/admin/applications?skip=0&limit=10" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

## 📊 Database Models

### User Model
```python
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique, Email)
- full_name: String
- hashed_password: String
- is_active: Boolean
- is_admin: Boolean
- created_at: DateTime
- updated_at: DateTime
- applications: Relationship to Application
- refresh_tokens: Relationship to RefreshToken
```

### Application Model
```python
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key to User)
- name: String
- email: String
- phone: String
- skills: Array of Strings
- experience_years: Integer
- position: String
- cover_letter: Text (Optional)
- status: String (pending, reviewing, accepted, rejected)
- rating: Float (0-5)
- notes: Text (Admin only)
- submitted_at: DateTime
- updated_at: DateTime
- user: Relationship to User
```

### RefreshToken Model
```python
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key to User)
- token: String (Unique)
- is_revoked: Boolean
- created_at: DateTime
- expires_at: DateTime
- user: Relationship to User
```

## 🧪 Testing

### Run Comprehensive Test Suite

```bash
# Install requests library
pip install requests

# Run tests (make sure API server is running)
python test_api_comprehensive.py
```

The test suite covers:
- User registration
- User login
- Token refresh
- Application submission
- Retrieving applications
- Filtering and searching
- Updating applications
- Deleting applications
- Logout

### Manual Testing with Swagger UI

1. Go to http://localhost:8000/docs
2. Register a new user using `/auth/register`
3. Login using `/auth/login`
4. Copy the `access_token`
5. Click "Authorize" button and enter: `Bearer YOUR_ACCESS_TOKEN`
6. Test all endpoints with the interactive UI

## 🗄️ Database Configuration

### SQLite (Default - Development)

```env
DATABASE_URL=sqlite:///./job_applications.db
```

Database file will be created automatically in the project directory.

### PostgreSQL (Production)

1. Install PostgreSQL and create a database:
```bash
createdb job_app_db
```

2. Update `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/job_app_db
```

3. Install psycopg2:
```bash
pip install psycopg2-binary
```

## 📁 Project Structure

```
JOB_APP_API/
├── main.py                      # Main FastAPI application
├── models.py                    # SQLAlchemy models (User, Application, RefreshToken)
├── schemas.py                   # Pydantic validation schemas
├── database.py                  # Database configuration and utilities
├── security.py                  # Authentication and authorization utilities
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore file
├── test_api_comprehensive.py    # Comprehensive test suite
├── test_api.py                  # Basic test script
├── setup.bat                    # Windows setup script
├── run.bat                      # Windows run script
├── README.md                    # This file
└── QUICKSTART.md               # Quick start guide
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

## 🚀 Deployment

### Using Gunicorn (Production)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```bash
# Build image
docker build -t job-app-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e SECRET_KEY="your-secret-key" \
  job-app-api
```

### Using Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/job_app_db
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: job_app_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 📈 Future Enhancements

- [ ] Email notifications for application updates
- [ ] File upload support for resumes/portfolios
- [ ] Application timeline/status history
- [ ] Interview scheduling
- [ ] Email templates customization
- [ ] Bulk operations (import/export)
- [ ] Application analytics dashboard
- [ ] Two-factor authentication (2FA)
- [ ] OAuth2 social login integration
- [ ] GraphQL endpoint
- [ ] WebSocket real-time notifications
- [ ] Rate limiting per user
- [ ] Advanced search with Elasticsearch

## 🐛 Troubleshooting

### "Database is locked" error (SQLite)

This typically happens with concurrent access. Solution:
- Use PostgreSQL for production
- Or implement connection pooling for SQLite

### "Invalid token" error

- Check if token is expired (30 minutes)
- Use refresh endpoint to get new access token
- Ensure token is in correct format: `Bearer TOKEN`

### "Permission denied" error

- User is trying to access another user's data
- Check if user has admin role for admin endpoints
- Use `/auth/logout` and re-login if needed

### Module not found errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or use --force-reinstall
pip install --force-reinstall -r requirements.txt
```

## 📞 Support & Documentation

- Full API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- Test suite: `python test_api_comprehensive.py`

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

---

**Created:** November 2024  
**Version:** 2.0.0 (with authentication & database)

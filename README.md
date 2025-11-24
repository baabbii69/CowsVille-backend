# Cowsville Farm Management System

A comprehensive Django REST Framework application for farm and veterinary management.

## 🚀 Features

- **Farm Management**: Track farms, cows, and livestock data
- **Veterinary Records**: Medical assessments, treatments, and health monitoring
- **Breeding Management**: Insemination records, reproduction tracking
- **Alert System**: Automated alerts for heat signs and pregnancy checks
- **SMS Integration**: Afromessage SMS service integration
- **RESTful API**: Complete API with Swagger documentation
- **Admin Panel**: Django admin interface for data management

## 📋 Requirements

- Python 3.13+
- PostgreSQL 12+
- Nginx (for production)
- Gunicorn (for production)

## 🛠️ Local Development Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd CowsVille-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your local configuration.

### 5. Set Up Database

```bash
# Create PostgreSQL database
psql -U postgres
CREATE USER farmuser WITH PASSWORD 'farm123';
CREATE DATABASE farmmanager OWNER farmuser;
ALTER USER farmuser CREATEDB;
\q
```

### 6. Run Migrations

```bash
python manage.py migrate
python manage.py populate_choices
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
# With DEBUG=True (local development)
python manage.py runserver

# With DEBUG=False (testing production settings)
python manage.py runserver --insecure
```

### 9. Access Application

- **API Root**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/swagger/

## 🚢 VPS Deployment

See [VPS_DEPLOYMENT_GUIDE.md](VPS_DEPLOYMENT_GUIDE.md) for complete deployment instructions.

### Quick Deployment Steps

1. SSH into VPS
2. Install dependencies (Python, PostgreSQL, Nginx)
3. Clone repository
4. Set up virtual environment
5. Configure `.env` file
6. Run migrations and collect static files
7. Set up Gunicorn service
8. Configure Nginx
9. Start services

## 📁 Project Structure

```
CowsVille-backend/
├── FarmManager/          # Main app (models, views, serializers)
├── AlertSystem/          # Alert checking logic
├── FarmManagerSystem/    # Project settings
├── logs/                 # Application logs
├── media/                # User uploads
├── staticfiles/          # Collected static files
├── gunicorn_config.py    # Gunicorn configuration
├── cowsville.service     # Systemd service file
├── nginx_cowsville.conf  # Nginx configuration
├── start.sh              # Gunicorn startup script
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

## 🔧 Configuration Files

- **`.env`**: Environment variables (not in Git)
- **`.env.example`**: Template for environment variables
- **`gunicorn_config.py`**: Gunicorn server settings
- **`cowsville.service`**: Systemd service configuration
- **`nginx_cowsville.conf`**: Nginx reverse proxy configuration

## 📝 Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings
DB_NAME=farmmanager
DB_USER=farmuser
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=your-domain.com,your-ip
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Check deployment readiness
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput
```

## 📚 API Documentation

API documentation is available via Swagger UI:

- Local: http://127.0.0.1:8000/swagger/
- Production: http://your-domain/swagger/

## 🔐 Security

- All sensitive data in `.env` file (not committed to Git)
- HTTPS enabled in production
- CORS configured for allowed origins
- CSRF protection enabled
- Secure cookie settings in production

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Verify database exists
sudo -u postgres psql -l
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Service Not Starting

```bash
# Check logs
sudo journalctl -u cowsville -n 50
tail -f logs/gunicorn_error.log
```

## 📞 Support

For issues and questions, please contact the development team.

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Team Information]

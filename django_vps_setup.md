# Django Project Refactor and VPS-Ready Setup Guide

## Purpose
This document prepares the Django project for:
- Local development using PostgreSQL  
- VPS deployment (Ubuntu + Gunicorn + Nginx)  
- Full migration away from MySQL  
- Clean environment variable management  
- Unfold Admin installation  
- Code cleanup and modernization  

It is designed to be uploaded into an AI code editor (Cursor, Windsurf, Antigravity, etc.).

---

## 1. Convert Entire Project to PostgreSQL

Update `DATABASES` in:
- `settings.py`
- `productions_settings.py`

Use:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}
```

Remove **all** MySQL code everywhere in the project.

---

## 2. Create `.env.example`

```env
# ----------------------------
# DJANGO SETTINGS
# ----------------------------
DEBUG=True
DJANGO_SECRET_KEY=
DJANGO_SETTINGS_MODULE=FarmManagerSystem.settings

# ----------------------------
# DATABASE (POSTGRES)
# ----------------------------
DB_ENGINE=postgresql
DB_NAME=farmmanager
DB_USER=farmuser
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# ----------------------------
# SECURITY
# ----------------------------
ALLOWED_HOSTS=localhost,127.0.0.1,api.local
SECURE_SSL_REDIRECT=False

# ----------------------------
# CORS
# ----------------------------
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,*

# ----------------------------
# AFROMESSAGE SMS SERVICE
# ----------------------------
AFROMESSAGE_API_TOKEN=
AFROMESSAGE_SENDER_NAME=Cowsville
```

---

## 3. Clean and Rewrite `.env`

Your real `.env` must look like this:

```env
# ----------------------------
# AFROMESSAGE SMS API
# ----------------------------
AFROMESSAGE_API_TOKEN=your-token-here
AFROMESSAGE_SENDER_NAME=Cowsville

# ----------------------------
# DJANGO
# ----------------------------
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings

# ----------------------------
# POSTGRES DATABASE
# ----------------------------
DB_ENGINE=postgresql
DB_NAME=cowsville_db
DB_USER=cowsville_user
DB_PASSWORD=replace-me
DB_HOST=localhost
DB_PORT=5432

# ----------------------------
# HOSTS
# ----------------------------
ALLOWED_HOSTS=localhost,127.0.0.1,api.cowsville-aau-cvma.com,apiv3.cowsville-aau-cvma.com

# ----------------------------
# CORS CONFIG
# ----------------------------
CORS_ALLOWED_ORIGINS=https://cowsville-aau-cvma.com,https://www.cowsville-aau-cvma.com,http://localhost:3000,*
SECURE_SSL_REDIRECT=False
```

---

## 4. Update `.gitignore`

```
.env
*.pyc
__pycache__/
staticfiles/
media/
logs/
```

---

## 5. Remove Unused and Incorrect Code

Your AI editor must:
- Remove all MySQL logic
- Remove APScheduler or broken cronjob logic
- Remove unused imports
- Remove dead code or unreachable logic
- Clean up unused variables
- Ensure all `.env` variables are loaded properly

---

## 6. Install & Configure Unfold Admin

Enable in `INSTALLED_APPS` then add:

```python
UNFOLD = {
    "site_title": "Cowsville Management",
    "site_header": "Cowsville Admin",
    "site_logo": "icons/logo.svg",
    "show_history": True,
    "collapsible_menu": True,
    "colors": {
        "primary": "#134B73",
    },
}
```

Static settings:

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Place logo in:

```
FarmManagerSystem/static/icons/logo.svg
```

---

## 7. Add PostgreSQL Setup Commands (for VPS)

Add this to README:

```bash
psql -U postgres -c "CREATE USER farmuser WITH PASSWORD 'farm123';"
psql -U postgres -c 'CREATE DATABASE farmmanager OWNER farmuser;'
```

---

## 8. Create `start.sh` for VPS

```bash
#!/bin/bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings
gunicorn FarmManagerSystem.wsgi:application --bind 0.0.0.0:8000
```

Make executable:

```bash
chmod +x start.sh
```

---

## 9. Mandatory Tasks for the AI Editor

The editor must:

- Run `black` and `isort` formatting  
- Apply consistent import sorting  
- Update all settings to use environment variables  
- Clean any hard-coded file paths  
- Fix SMS API integration to load from `.env`  
- Verify all migrations are working  
- Generate a summary of changes made  

---

## End of File

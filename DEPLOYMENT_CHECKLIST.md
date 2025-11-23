# 🚀 Deployment Checklist - Ready to Zip and Upload

## ✅ Pre-Deployment Verification

### 1. **Database Configuration**
- [x] SQLite removed from all settings
- [x] MySQL configured in both `settings.py` and `productions_settings.py`
- [x] Environment variables properly configured
- [x] Database credentials match cPanel

### 2. **Dependencies**
- [x] `requirements.txt` includes all necessary packages
- [x] `requirements-prod.txt` created for production (optional)
- [x] PyMySQL installed for MySQL support
- [x] All packages tested and working

### 3. **Environment Variables**
- [x] `.env` file created with production credentials
- [x] `env.example` template available
- [x] `.env` is in `.gitignore` (won't be committed)

### 4. **Settings Files**
- [x] `settings.py` uses MySQL (no SQLite)
- [x] `productions_settings.py` configured for production
- [x] Security settings enabled in production
- [x] CORS properly configured

### 5. **WSGI Configuration**
- [x] `wsgi.py` updated for production
- [x] `passenger_wsgi.py` created for cPanel
- [x] Environment variable loading configured

### 6. **Static Files**
- [x] `STATIC_ROOT` configured
- [x] `MEDIA_ROOT` configured
- [x] Ready for `collectstatic`

### 7. **Files to Exclude from Deployment**
- [x] `.env` (contains sensitive data - create on server)
- [x] `db.sqlite3` (if exists, not needed)
- [x] `__pycache__/` directories
- [x] `.venv/` or `venv/` (virtual environment)
- [x] `*.pyc` files
- [x] `.git/` directory (optional)

## 📦 Files to Include in Deployment Zip

### Required Files:
```
├── FarmManager/              # Main app
├── FarmManagerSystem/        # Project settings
│   ├── settings.py
│   ├── productions_settings.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── urls.py
│   └── passenger_wsgi.py    # For cPanel
├── AlertSystem/              # Alert system
├── manage.py
├── requirements.txt          # Or requirements-prod.txt
├── passenger_wsgi.py         # Root level (if needed)
├── gunicorn_config.py        # If using Gunicorn
├── .gitignore
└── env.example               # Template for .env
```

### Optional but Recommended:
```
├── DEPLOYMENT_GUIDE.md
├── DEPLOYMENT_CHECKLIST.md
├── LOCAL_SETUP.md
└── README.md (if exists)
```

## 🔧 Pre-Zip Steps

### 1. **Clean Up**
```bash
# Remove SQLite database if exists
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows

# Remove __pycache__ directories
find . -type d -name __pycache__ -exec rm -r {} +  # Linux/Mac
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force  # Windows

# Remove .pyc files
find . -name "*.pyc" -delete  # Linux/Mac
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force  # Windows
```

### 2. **Collect Static Files** (Optional - can do on server)
```bash
python manage.py collectstatic --noinput
```

### 3. **Verify .env is Excluded**
Make sure `.env` is in `.gitignore` and won't be included in the zip.

## 📤 Creating Deployment Zip

### Windows PowerShell:
```powershell
# Exclude unnecessary files
$exclude = @('*.pyc', '__pycache__', '.venv', 'venv', '.git', 'db.sqlite3', '.env')
Compress-Archive -Path * -DestinationPath ../cowsville-deployment.zip -Exclude $exclude
```

### Linux/Mac:
```bash
zip -r ../cowsville-deployment.zip . \
  -x "*.pyc" \
  -x "__pycache__/*" \
  -x ".venv/*" \
  -x "venv/*" \
  -x ".git/*" \
  -x "db.sqlite3" \
  -x ".env"
```

### Manual Method:
1. Select all project files
2. Exclude: `.venv/`, `__pycache__/`, `.git/`, `db.sqlite3`, `.env`
3. Create zip file

## 🚀 cPanel Deployment Steps

### 1. **Upload Files**
- Upload the zip file to cPanel
- Extract in your domain directory (e.g., `public_html/` or subdirectory)

### 2. **Create .env File on Server**
Create `.env` file on the server with your production credentials:
```env
# Django Settings
DJANGO_SECRET_KEY=<generate-new-secret-key>
DEBUG=False
DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings

# Allowed Hosts
ALLOWED_HOSTS=cowsville-aau-cvma.com,www.cowsville-aau-cvma.com,api.cowsville-aau-cvma.com

# Database Settings - MySQL
DB_ENGINE=mysql
DB_NAME=cowsvijp_cowsville
DB_USER=cowsvijp_admin
DB_PASSWORD=SecurePass123
DB_HOST=localhost
DB_PORT=3306

# CORS Settings
CORS_ALLOWED_ORIGINS=https://cowsville-aau-cvma.com,https://www.cowsville-aau-cvma.com

# Security
SECURE_SSL_REDIRECT=True

# SMS/Alert System
AFROMESSAGE_API_TOKEN=your_token_here
AFROMESSAGE_SENDER_NAME=Cowsville
```

### 3. **Set Up Python App in cPanel**
1. Go to "Setup Python App" in cPanel
2. Create new application
3. Python version: 3.10+ (check available versions)
4. Application root: `/home/username/yourdomain.com`
5. Application URL: `/` or `/api`
6. Application startup file: `passenger_wsgi.py`

### 4. **Install Dependencies**
In cPanel Python App:
```bash
pip install -r requirements.txt
```

Or use `requirements-prod.txt` for production:
```bash
pip install -r requirements-prod.txt
```

### 5. **Set Environment Variables**
In cPanel Python App settings, add:
- `DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings`
- Or set in `.env` file (recommended)

### 6. **Run Migrations**
Using cPanel Terminal or SSH:
```bash
cd /home/username/yourdomain.com
source venv/bin/activate  # If using virtual env
python manage.py migrate
python manage.py populate_choices
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 7. **Set File Permissions**
```bash
chmod 755 manage.py
chmod 644 *.py
chmod 600 .env
chmod -R 755 staticfiles/
chmod -R 755 media/
```

### 8. **Restart Application**
In cPanel Python App, click "Restart" to apply changes.

## ✅ Post-Deployment Verification

1. **Test Database Connection**:
   ```bash
   python manage.py check --database default
   ```

2. **Test API Endpoints**:
   - Visit: `https://yourdomain.com/api/`
   - Visit: `https://yourdomain.com/swagger/`

3. **Test Admin Panel**:
   - Visit: `https://yourdomain.com/admin/`
   - Login with superuser credentials

4. **Check Logs**:
   - Check `logs/farm_manager.log` for errors
   - Check cPanel error logs

## 🔒 Security Checklist

- [ ] `.env` file has correct permissions (600)
- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is strong and unique
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] SSL/HTTPS is enabled
- [ ] `SECURE_SSL_REDIRECT=True` in production
- [ ] Database credentials are secure
- [ ] `.env` is not publicly accessible

## 📝 Quick Reference

### Generate New Secret Key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Test Production Settings Locally:
```bash
set DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings
python manage.py check --deploy
```

### Common Commands:
```bash
# Migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Populate choices
python manage.py populate_choices

# Create sample data
python manage.py create_sample_data
```

---

**Status**: ✅ Ready for Deployment
**Database**: MySQL (no SQLite)
**Python**: 3.10+
**Django**: 5.2.8


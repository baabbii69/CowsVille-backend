# Django REST Framework - cPanel Deployment Guide

## 🚀 Project Setup Complete

Your Django project has been configured for optimal deployment on shared hosting (cPanel). Here's what has been set up:

## ✅ What's Been Configured

### 1. **Environment Variables**
- ✅ Settings now use environment variables via `.env` file
- ✅ `env.example` template created for reference
- ✅ SECRET_KEY moved to environment variables (security improvement)

### 2. **Production Settings**
- ✅ Enhanced `productions_settings.py` with:
  - Security headers (SSL, XSS protection, etc.)
  - Database configuration for PostgreSQL/MySQL/SQLite
  - Proper static files configuration
  - Production logging
  - CORS restrictions

### 3. **WSGI Configuration**
- ✅ `wsgi.py` updated to use production settings by default
- ✅ Environment variable loading added

### 4. **Procfile**
- ✅ Fixed path from `Cowsville.wsgi` to `FarmManagerSystem.wsgi`

## 📋 Pre-Deployment Checklist

### Step 1: Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Create `.env` File
Copy `env.example` to `.env` and fill in your values:
```bash
cp env.example .env
```

Required variables for production:
```env
DJANGO_SECRET_KEY=<generated-secret-key>
DEBUG=False
DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings
ALLOWED_HOSTS=cowsville-aau-cvma.com,www.cowsville-aau-cvma.com,api.cowsville-aau-cvma.com
DB_ENGINE=postgresql  # or mysql
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432  # or 3306 for MySQL
CORS_ALLOWED_ORIGINS=https://cowsville-aau-cvma.com,https://www.cowsville-aau-cvma.com
SECURE_SSL_REDIRECT=True
```

### Step 3: Database Setup
**For PostgreSQL (Recommended):**
```bash
# Install PostgreSQL adapter (already in requirements.txt)
# Create database in cPanel
# Run migrations
python manage.py migrate
```

**For MySQL:**
```bash
# Install MySQL adapter if needed
pip install mysqlclient  # or use pymysql
# Create database in cPanel
# Run migrations
python manage.py migrate
```

### Step 4: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

## 🎯 cPanel Deployment Steps

### Option 1: Using Passenger (Recommended for cPanel)

1. **Upload Files**
   - Upload your project to `public_html` or a subdirectory
   - Ensure `.env` file is uploaded (but not publicly accessible)

2. **Configure Python App**
   - In cPanel, go to "Setup Python App"
   - Create a new application
   - Python version: 3.9+ (check what's available)
   - Application root: `/home/username/yourdomain.com`
   - Application URL: `/` or `/api` (depending on your setup)
   - Application startup file: `passenger_wsgi.py` (create this)

3. **Create `passenger_wsgi.py`**
   ```python
   import sys
   import os
   from pathlib import Path
   
   # Add your project directory to Python path
   project_dir = Path(__file__).resolve().parent
   sys.path.insert(0, str(project_dir))
   
   # Set environment variables
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagerSystem.productions_settings')
   
   # Load environment variables from .env
   from dotenv import load_dotenv
   load_dotenv()
   
   # Import Django WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

4. **Install Dependencies**
   - In cPanel Python App, go to "Manage Python Packages"
   - Install from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Or use the cPanel interface to install packages

5. **Set Environment Variables**
   - In cPanel Python App settings, add environment variables:
     - `DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings`
     - `DJANGO_SECRET_KEY=your-secret-key`
     - `DB_NAME=your_db_name`
     - etc.

6. **Run Migrations**
   - Use cPanel Terminal or SSH:
   ```bash
   cd /home/username/yourdomain.com
   source venv/bin/activate  # if using virtual env
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

### Option 2: Using Gunicorn + Nginx (If Available)

1. **Install Gunicorn** (add to requirements.txt if not present):
   ```bash
   pip install gunicorn
   ```

2. **Create `gunicorn_config.py`**:
   ```python
   bind = "127.0.0.1:8000"
   workers = 2  # Adjust based on server resources
   worker_class = "sync"
   timeout = 30
   keepalive = 2
   max_requests = 1000
   max_requests_jitter = 50
   ```

3. **Run Gunicorn**:
   ```bash
   gunicorn -c gunicorn_config.py FarmManagerSystem.wsgi:application
   ```

4. **Configure Nginx** (if you have access):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /path/to/your/project/staticfiles/;
       }
       
       location /media/ {
           alias /path/to/your/project/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

## 🔒 Security Best Practices for cPanel

### 1. **File Permissions**
```bash
# Set proper permissions
chmod 755 manage.py
chmod 644 *.py
chmod 600 .env  # Keep .env private
chmod -R 755 staticfiles/
chmod -R 755 media/
```

### 2. **.htaccess for Static Files** (if needed)
Create `.htaccess` in `staticfiles/`:
```apache
<IfModule mod_headers.c>
    Header set Cache-Control "max-age=31536000, public"
</IfModule>
```

### 3. **Protect Sensitive Files**
Ensure `.env`, `db.sqlite3`, and other sensitive files are not web-accessible.

### 4. **SSL/HTTPS**
- Enable SSL certificate in cPanel
- Set `SECURE_SSL_REDIRECT=True` in production
- Update `ALLOWED_HOSTS` to match your domain

## 📊 Resource Optimization for Shared Hosting

### 1. **Database Optimization**
- ✅ Connection pooling enabled (`CONN_MAX_AGE=600`)
- ✅ Query timeouts configured
- ✅ Use PostgreSQL or MySQL instead of SQLite for production

### 2. **Caching**
- Currently using `LocMemCache` (in-memory)
- For better performance, consider Redis (if available):
  ```python
  CACHES = {
      'default': {
          'BACKEND': 'django.core.cache.backends.redis.RedisCache',
          'LOCATION': 'redis://127.0.0.1:6379/1',
      }
  }
  ```

### 3. **Static Files**
- ✅ `STATIC_ROOT` configured for `collectstatic`
- Serve static files via web server (Nginx/Apache) not Django
- Use CDN for static assets if possible

### 4. **Request Throttling**
- ✅ Already configured in `REST_FRAMEWORK` settings:
  - Anonymous: 100 requests/hour
  - Authenticated: 1000 requests/hour

### 5. **Pagination**
- ✅ Default page size: 50 items
- ✅ Prevents loading all records at once

### 6. **Worker Processes**
For Gunicorn, use 2-4 workers on shared hosting:
```python
workers = 2  # Start with 2, increase if resources allow
```

### 7. **Memory Management**
- Monitor memory usage
- Use `max_requests` in Gunicorn to restart workers periodically
- Consider using `--preload` flag for better memory sharing

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path in `passenger_wsgi.py`

2. **Database Connection Errors**
   - Verify database credentials in `.env`
   - Check database host (might be `localhost` or specific IP)
   - Ensure database user has proper permissions

3. **Static Files Not Loading**
   - Run `collectstatic`
   - Check `STATIC_ROOT` path
   - Verify web server configuration

4. **500 Errors**
   - Check logs: `logs/farm_manager.log`
   - Enable DEBUG temporarily to see errors
   - Check file permissions

5. **CORS Errors**
   - Verify `CORS_ALLOWED_ORIGINS` includes your frontend domain
   - Check if `CORS_ALLOW_ALL_ORIGINS` is False in production

## 📝 Additional Recommendations

### 1. **Monitoring**
- Set up error tracking (Sentry, etc.)
- Monitor log files regularly
- Set up uptime monitoring

### 2. **Backups**
- Regular database backups
- Backup `.env` file securely
- Version control all code changes

### 3. **Performance Monitoring**
- Use Django's built-in performance middleware (already configured)
- Monitor slow queries
- Check request timeouts

### 4. **Updates**
- Keep Django and dependencies updated
- Security patches should be applied promptly
- Test updates in staging first

## 🔍 Pre-Deployment Testing

Before deploying to production:

1. **Test Locally with Production Settings**:
   ```bash
   export DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings
   python manage.py check --deploy
   python manage.py migrate
   python manage.py collectstatic
   python manage.py runserver
   ```

2. **Run Django Deployment Checklist**:
   ```bash
   python manage.py check --deploy
   ```

3. **Test API Endpoints**:
   - Verify all endpoints work
   - Check authentication
   - Test pagination
   - Verify CORS headers

4. **Load Testing** (if possible):
   - Test with expected traffic
   - Monitor memory usage
   - Check response times

## 📞 Support

If you encounter issues:
1. Check `logs/farm_manager.log`
2. Review cPanel error logs
3. Verify environment variables
4. Test database connectivity
5. Check file permissions

---

**Last Updated**: After initial setup
**Project**: Cowsville Farm Management System
**Framework**: Django 5.2.8 + Django REST Framework


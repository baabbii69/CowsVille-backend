# 🚀 Quick Deployment Guide - cPanel Shared Hosting

## ✅ Everything is Ready!

All files are configured and ready. Deployment is now simple:

## 📦 Step 1: Create Deployment Zip

### Windows (PowerShell):

```powershell
# Navigate to project directory
cd "C:\Users\baabbii\Documents\Code\django\for deployment"

# Create zip excluding unnecessary files
$exclude = @('*.pyc', '__pycache__', '.venv', 'venv', '.git', 'db.sqlite3', '.env', '*.log', 'setup_mysql_local.py', 'LOCAL_SETUP.md', 'MYSQL_SETUP_COMPLETE.md')
Get-ChildItem -Path . -Exclude $exclude | Compress-Archive -DestinationPath ..\cowsville-deployment.zip -Force
```

### Or Manual Method:

1. Select all files and folders
2. **EXCLUDE**: `.venv/`, `__pycache__/`, `.git/`, `.env`, `*.log`, `setup_mysql_local.py`
3. Right-click → Send to → Compressed (zipped) folder
4. Name it `cowsville-deployment.zip`

## 📤 Step 2: Upload to cPanel

1. Login to cPanel
2. Go to **File Manager**
3. Navigate to your domain directory (usually `public_html/` or a subdirectory)
4. Upload `cowsville-deployment.zip`
5. Right-click zip → **Extract**
6. Delete the zip file after extraction

## ⚙️ Step 3: Create .env File on Server

In cPanel File Manager, create `.env` file in project root:

```env
DJANGO_SECRET_KEY=<generate-new-secret-key>
DEBUG=False
DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings
ALLOWED_HOSTS=cowsville-aau-cvma.com,www.cowsville-aau-cvma.com,api.cowsville-aau-cvma.com
DB_ENGINE=mysql
DB_NAME=cowsvijp_cowsville
DB_USER=cowsvijp_admin
DB_PASSWORD=SecurePass123
DB_HOST=localhost
DB_PORT=3306
CORS_ALLOWED_ORIGINS=https://cowsville-aau-cvma.com,https://www.cowsville-aau-cvma.com
SECURE_SSL_REDIRECT=True
AFROMESSAGE_API_TOKEN=your_token_here
AFROMESSAGE_SENDER_NAME=Cowsville
```

**Generate Secret Key:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🐍 Step 4: Set Up Python App

1. In cPanel, go to **"Setup Python App"**
2. Click **"Create Application"**
3. Fill in:
   - **Python Version**: 3.10 or higher
   - **Application Root**: `/home/username/yourdomain.com` (or subdirectory)
   - **Application URL**: `/` (or `/api` if subdirectory)
   - **Application Startup File**: `passenger_wsgi.py`
4. Click **"Create"**

## 📦 Step 5: Install Dependencies

In the Python App interface:

1. Click **"Manage Python Packages"**
2. Run:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Step 6: Run Setup Commands

Using cPanel **Terminal** or **SSH**:

```bash
cd /home/username/yourdomain.com
python manage.py migrate
python manage.py populate_choices
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 🔐 Step 7: Set Permissions

In cPanel File Manager or Terminal:

```bash
chmod 755 manage.py
chmod 644 *.py
chmod 600 .env
chmod -R 755 staticfiles/
chmod -R 755 media/
chmod -R 755 logs/
```

## 🔄 Step 8: Restart Application

In cPanel Python App, click **"Restart"**

## ✅ Step 9: Verify

1. **API**: `https://yourdomain.com/api/`
2. **Swagger**: `https://yourdomain.com/swagger/`
3. **Admin**: `https://yourdomain.com/admin/`
4. **Logs**: Check `logs/farm_manager.log` for errors

## 🎉 Done!

Your Django application is now live on cPanel!

## 🆘 Troubleshooting

### Issue: 500 Error

- Check `logs/farm_manager.log`
- Verify `.env` file exists and has correct values
- Check file permissions
- Restart Python App

### Issue: Static Files Not Loading

- Run `python manage.py collectstatic --noinput`
- Check `staticfiles/` directory exists
- Verify `.htaccess` files are in place

### Issue: Database Connection Error

- Verify database credentials in `.env`
- Check database exists in cPanel
- Verify database user has proper permissions

### Issue: Import Errors

- Verify all packages installed: `pip install -r requirements.txt`
- Check Python version (3.10+)
- Restart Python App

---

**That's it!** The deployment is now as simple as: Zip → Upload → Create .env → Install → Migrate → Restart

# VPS Deployment Guide for Cowsville

**Server:** Alemayehu  
**IP:** 78.47.170.156  
**User:** root

---

## Prerequisites

- SSH access to VPS (root@78.47.170.156)
- Git repository with your code
- New SECRET*KEY: `dd)fd+v47h6s0&72n1(32(j)$t#to!tkbaer@*@ssavmj5_vx@`

---

## Step 1: Connect to VPS

```bash
ssh root@78.47.170.156
```

---

## Step 2: Update System and Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Python 3.13 (or latest available)
apt install -y python3 python3-venv python3-pip python3-dev

# Install PostgreSQL
apt install -y postgresql postgresql-contrib libpq-dev

# Install Nginx
apt install -y nginx

# Install other dependencies
apt install -y git build-essential
```

---

## Step 3: Set Up PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt, run:
CREATE USER farmuser WITH PASSWORD 'YOUR_SECURE_PASSWORD_HERE';
CREATE DATABASE farmmanager OWNER farmuser;
ALTER USER farmuser CREATEDB;
\q
```

**Important:** Replace `YOUR_SECURE_PASSWORD_HERE` with a strong password and save it!

---

## Step 4: Clone Repository

```bash
# Navigate to root home directory
cd /root

# Clone your repository
git clone https://github.com/YOUR_USERNAME/CowsVille-backend.git
# OR if using different Git hosting:
# git clone YOUR_REPO_URL CowsVille-backend

cd CowsVille-backend
```

---

## Step 5: Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## Step 6: Configure Environment Variables

```bash
# Create .env file
nano .env
```

**Paste this content (update the values):**

```env
# ----------------------------
# AFROMESSAGE SMS API
# ----------------------------
AFROMESSAGE_API_TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiY01iNFNzeW1QSDZDTDkwOUt2RzNTOEh6VjRoQ2NmRzIiLCJleHAiOjE5MDYxODc0MjIsImlhdCI6MTc0ODQyMTAyMiwianRpIjoiN2MxYzQ0MTEtYjgwYS00ZGNjLThlYTMtN2FmMzA3NmQ5YTI3In0.cgNrAyjr4IUuQM1nNqgEjzoWwu96uBw4yzc9eAjANXw
AFROMESSAGE_SENDER_NAME=Cowsville

# ----------------------------
# DJANGO
# ----------------------------
DEBUG=False
DJANGO_SECRET_KEY=dd)fd+v47h6s0&72n1(32(j)$t#to!tkbaer@_@ssavmj5_vx@
DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings

# ----------------------------
# POSTGRES DATABASE
# ----------------------------
DB_ENGINE=postgresql
DB_NAME=farmmanager
DB_USER=farmuser
DB_PASSWORD=YOUR_SECURE_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=5432

# ----------------------------
# HOSTS
# ----------------------------
ALLOWED_HOSTS=localhost,127.0.0.1,78.47.170.156

# ----------------------------
# CORS CONFIG
# ----------------------------
CORS_ALLOWED_ORIGINS=http://78.47.170.156,http://localhost:3000,*

# ----------------------------
# SECURITY
# ----------------------------
SECURE_SSL_REDIRECT=False
```

**Save and exit:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 7: Run Django Setup

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Create logs directory
mkdir -p logs

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Follow prompts to create admin account

# Collect static files
python manage.py collectstatic --noinput

# Populate choice models (if needed)
python manage.py populate_choices
```

---

## Step 8: Test Gunicorn

```bash
# Test Gunicorn manually
gunicorn --config gunicorn_config.py FarmManagerSystem.wsgi:application

# If it works, press Ctrl+C to stop
```

---

## Step 9: Set Up Systemd Service

```bash
# Copy service file
cp cowsville.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable service to start on boot
systemctl enable cowsville

# Start the service
systemctl start cowsville

# Check status
systemctl status cowsville
```

---

## Step 10: Configure Nginx

```bash
# Copy Nginx configuration
cp nginx_cowsville.conf /etc/nginx/sites-available/cowsville

# Create symbolic link
ln -s /etc/nginx/sites-available/cowsville /etc/nginx/sites-enabled/

# Remove default site (optional)
rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# If test passes, restart Nginx
systemctl restart nginx
```

---

## Step 11: Configure Firewall

```bash
# Allow HTTP
ufw allow 80/tcp

# Allow HTTPS (for future)
ufw allow 443/tcp

# Allow SSH (IMPORTANT!)
ufw allow 22/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

---

## Step 12: Verify Deployment

Open your browser and visit:

- **API:** http://78.47.170.156/api/
- **Admin:** http://78.47.170.156/admin/

Login with the superuser credentials you created.

---

## Troubleshooting

### Check Gunicorn logs:

```bash
journalctl -u cowsville -f
tail -f /root/CowsVille-backend/logs/gunicorn_error.log
```

### Check Nginx logs:

```bash
tail -f /var/log/nginx/cowsville_error.log
tail -f /var/log/nginx/cowsville_access.log
```

### Restart services:

```bash
systemctl restart cowsville
systemctl restart nginx
```

### Check service status:

```bash
systemctl status cowsville
systemctl status nginx
systemctl status postgresql
```

---

## Common Issues

### 1. Static files not loading

```bash
cd /root/CowsVille-backend
source venv/bin/activate
python manage.py collectstatic --noinput
systemctl restart nginx
```

### 2. Database connection error

- Check PostgreSQL is running: `systemctl status postgresql`
- Verify database credentials in `.env`
- Check database exists: `sudo -u postgres psql -l`

### 3. Gunicorn won't start

- Check logs: `journalctl -u cowsville -n 50`
- Verify virtual environment path in service file
- Check `.env` file exists and has correct permissions

---

## Future: Adding Domain Name

When you purchase a domain:

1. **Update DNS records:**

   - Add A record pointing to `78.47.170.156`

2. **Update Nginx configuration:**

   ```bash
   nano /etc/nginx/sites-available/cowsville
   # Update server_name to your domain
   ```

3. **Install SSL certificate:**

   ```bash
   apt install certbot python3-certbot-nginx
   certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

4. **Update `.env`:**

   ```bash
   nano /root/CowsVille-backend/.env
   # Update ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS
   ```

5. **Restart services:**
   ```bash
   systemctl restart cowsville
   systemctl restart nginx
   ```

---

## Maintenance Commands

```bash
# Update code from Git
cd /root/CowsVille-backend
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart cowsville

# View logs
journalctl -u cowsville -f

# Database backup
sudo -u postgres pg_dump farmmanager > backup_$(date +%Y%m%d).sql

# Database restore
sudo -u postgres psql farmmanager < backup_YYYYMMDD.sql
```

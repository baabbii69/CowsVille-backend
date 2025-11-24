# VPS Deployment Instructions

## Step 1: Generated Production SECRET_KEY ✅

**New SECRET_KEY (SAVE THIS SECURELY):**

```
dd)fd+v47h6s0&72n1(32(j)$t#to!tkbaer@_@ssavmj5_vx@
```

**Action Required:**

- Update your `.env` file on the VPS with this new SECRET_KEY
- DO NOT commit this to Git
- Keep this secure

---

## Step 2: Deployment Check Results

**Issues Found:**

1. ⚠️ `DEBUG` should not be set to `True` in deployment
   - **Status:** Already configured correctly in `.env` (DEBUG=False)
   - **No action needed**

---

## Step 3: Configuration Files Created ✅

### 3.1 Gunicorn Configuration

- **File:** `gunicorn_config.py`
- **Location:** Project root
- **Workers:** Auto-calculated based on CPU cores
- **Logs:** `logs/gunicorn_access.log` and `logs/gunicorn_error.log`

### 3.2 Systemd Service

- **File:** `cowsville.service`
- **Location:** Project root (will be copied to `/etc/systemd/system/` on VPS)
- **Action Required:** Update placeholders:
  - `YOUR_VPS_USERNAME` → your VPS username
  - `/path/to/CowsVille-backend` → actual path on VPS

### 3.3 Nginx Configuration

- **File:** `nginx_cowsville.conf`
- **Location:** Project root (will be copied to `/etc/nginx/sites-available/` on VPS)
- **Action Required:** Update placeholders:
  - `/path/to/CowsVille-backend` → actual path on VPS
  - SSL certificate paths (after obtaining Let's Encrypt certificates)

---

## Next Steps

### On Your Local Machine:

1. ✅ Update `.env` with new SECRET_KEY (if testing locally)
2. ✅ Commit configuration files to Git (except `.env`)
3. ✅ Push to repository

### On VPS:

1. Install system dependencies
2. Clone repository
3. Set up virtual environment
4. Configure `.env` file
5. Install Gunicorn service
6. Configure Nginx
7. Obtain SSL certificates
8. Start services

---

## VPS Setup Commands (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.13 python3.13-venv python3-pip postgresql postgresql-contrib nginx git

# Create application user (optional but recommended)
sudo adduser cowsville
sudo usermod -aG sudo cowsville
su - cowsville

# Clone repository
cd /var/www
git clone <your-repo-url> CowsVille-backend
cd CowsVille-backend

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Set up PostgreSQL
sudo -u postgres psql
CREATE USER farmuser WITH PASSWORD 'YOUR_SECURE_PASSWORD';
CREATE DATABASE farmmanager OWNER farmuser;
ALTER USER farmuser CREATEDB;
\q

# Configure .env file
nano .env
# (paste your production .env content)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test Gunicorn
gunicorn --config gunicorn_config.py FarmManagerSystem.wsgi:application

# Install systemd service
sudo cp cowsville.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cowsville
sudo systemctl start cowsville
sudo systemctl status cowsville

# Configure Nginx
sudo cp nginx_cowsville.conf /etc/nginx/sites-available/cowsville
sudo ln -s /etc/nginx/sites-available/cowsville /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Obtain SSL certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d apiv3.cowsville-aau-cvma.com -d api.cowsville-aau-cvma.com

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## Verification

After deployment, verify:

- [ ] API accessible at https://apiv3.cowsville-aau-cvma.com/api/
- [ ] Admin accessible at https://apiv3.cowsville-aau-cvma.com/admin/
- [ ] Static files loading correctly
- [ ] HTTPS redirect working
- [ ] Gunicorn service running
- [ ] Nginx service running
- [ ] Database connections working

---

## Troubleshooting

### Check Gunicorn logs:

```bash
tail -f logs/gunicorn_error.log
sudo journalctl -u cowsville -f
```

### Check Nginx logs:

```bash
sudo tail -f /var/log/nginx/cowsville_error.log
```

### Restart services:

```bash
sudo systemctl restart cowsville
sudo systemctl restart nginx
```

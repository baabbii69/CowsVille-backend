# Cowsville VPS Operations & Maintenance Guide

**Server:** Alemayehu  
**IP:** 78.47.170.156  
**Status:** ✅ Production Ready

---

## 🌐 Live Application URLs

- **API**: http://78.47.170.156/api/
- **Admin Panel**: http://78.47.170.156/admin/
- **API Documentation**: http://78.47.170.156/swagger/

---

## 📊 Daily Operations

### Check System Health

```bash
# SSH into server
ssh root@78.47.170.156

# Check all services status
systemctl status cowsville
systemctl status nginx
systemctl status postgresql

# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top
```

### View Application Logs

```bash
# Real-time Gunicorn logs
journalctl -u cowsville -f

# Real-time application logs
tail -f /root/CowsVille-backend/logs/gunicorn_error.log
tail -f /root/CowsVille-backend/logs/gunicorn_access.log

# Nginx logs
tail -f /var/log/nginx/cowsville_error.log
tail -f /var/log/nginx/cowsville_access.log

# PostgreSQL logs
tail -f /var/log/postgresql/postgresql-14-main.log
```

---

## 🔄 Deploying Code Updates

### Standard Deployment Process

```bash
# 1. SSH into server
ssh root@78.47.170.156

# 2. Navigate to project directory
cd /root/CowsVille-backend

# 3. Activate virtual environment
source venv/bin/activate

# 4. Pull latest code from GitHub
git pull origin main

# 5. Install any new dependencies
pip install -r requirements.txt

# 6. Run database migrations
python manage.py migrate

# 7. Collect static files (if CSS/JS changed)
python manage.py collectstatic --noinput

# 8. Restart Gunicorn service
systemctl restart cowsville

# 9. Verify deployment
systemctl status cowsville
curl http://localhost:8000/api/
```

### Quick Update (Code Only, No Dependencies)

```bash
cd /root/CowsVille-backend
git pull origin main
systemctl restart cowsville
```

---

## 🔧 Service Management

### Restart Services

```bash
# Restart Django application
systemctl restart cowsville

# Restart Nginx
systemctl restart nginx

# Restart PostgreSQL
systemctl restart postgresql

# Restart all services
systemctl restart cowsville nginx postgresql
```

### Stop/Start Services

```bash
# Stop application
systemctl stop cowsville

# Start application
systemctl start cowsville

# Check if service is enabled (auto-start on boot)
systemctl is-enabled cowsville
```

### View Service Status

```bash
# Detailed status
systemctl status cowsville

# Check if running
systemctl is-active cowsville

# View recent logs
journalctl -u cowsville -n 50
```

---

## 🗄️ Database Management

### Database Backups

```bash
# Create backup
sudo -u postgres pg_dump farmmanager > backup_$(date +%Y%m%d_%H%M%S).sql

# Create compressed backup
sudo -u postgres pg_dump farmmanager | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup to specific location
sudo -u postgres pg_dump farmmanager > /root/backups/farmmanager_$(date +%Y%m%d).sql
```

### Restore Database

```bash
# Restore from backup
sudo -u postgres psql farmmanager < backup_20251124.sql

# Restore from compressed backup
gunzip -c backup_20251124.sql.gz | sudo -u postgres psql farmmanager
```

### Database Maintenance

```bash
# Connect to database
sudo -u postgres psql farmmanager

# Inside PostgreSQL shell:
# View all tables
\dt

# Check database size
SELECT pg_size_pretty(pg_database_size('farmmanager'));

# Vacuum database (cleanup)
VACUUM ANALYZE;

# Exit
\q
```

### Create Superuser

```bash
cd /root/CowsVille-backend
source venv/bin/activate
python manage.py createsuperuser
```

---

## 🔍 Troubleshooting

### Application Not Responding

```bash
# 1. Check if Gunicorn is running
systemctl status cowsville

# 2. Check logs for errors
journalctl -u cowsville -n 100

# 3. Restart service
systemctl restart cowsville

# 4. If still not working, check Nginx
systemctl status nginx
systemctl restart nginx
```

### 502 Bad Gateway Error

```bash
# This means Nginx can't connect to Gunicorn

# 1. Check if Gunicorn is running
systemctl status cowsville

# 2. Check if port 8000 is listening
netstat -tulpn | grep 8000

# 3. Restart Gunicorn
systemctl restart cowsville
```

### Static Files Not Loading

```bash
# 1. Collect static files
cd /root/CowsVille-backend
source venv/bin/activate
python manage.py collectstatic --noinput

# 2. Check permissions
chmod -R 755 /root/CowsVille-backend/staticfiles

# 3. Restart Nginx
systemctl restart nginx
```

### Database Connection Errors

```bash
# 1. Check if PostgreSQL is running
systemctl status postgresql

# 2. Test database connection
sudo -u postgres psql farmmanager

# 3. Check credentials in .env file
cat /root/CowsVille-backend/.env | grep DB_

# 4. Restart PostgreSQL
systemctl restart postgresql
```

### High Memory Usage

```bash
# 1. Check memory usage
free -h

# 2. Check which process is using memory
top

# 3. Restart Gunicorn (frees memory)
systemctl restart cowsville

# 4. If PostgreSQL is using too much memory
systemctl restart postgresql
```

---

## 📈 Scaling & Performance

### Increase Gunicorn Workers

```bash
# Edit service file
nano /etc/systemd/system/cowsville.service

# Change --workers value (current: 4)
# Recommended: (2 x CPU cores) + 1
# For 2 CPU cores: --workers 5
# For 4 CPU cores: --workers 9

# Reload and restart
systemctl daemon-reload
systemctl restart cowsville
```

### Monitor Performance

```bash
# Real-time resource monitoring
htop

# Check active connections
netstat -an | grep :80 | wc -l

# Check Gunicorn worker processes
ps aux | grep gunicorn

# Database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
```

### Optimize Database

```bash
# Connect to database
sudo -u postgres psql farmmanager

# Analyze query performance
EXPLAIN ANALYZE SELECT * FROM your_table;

# Rebuild indexes
REINDEX DATABASE farmmanager;

# Update statistics
ANALYZE;
```

---

## 🔐 Security Maintenance

### Update System Packages

```bash
# Update package list
apt update

# Upgrade packages
apt upgrade -y

# Reboot if kernel updated
reboot
```

### Check Firewall Status

```bash
# View firewall rules
ufw status

# View detailed rules
ufw status verbose
```

### Monitor Failed Login Attempts

```bash
# Check auth logs
tail -f /var/log/auth.log

# Count failed SSH attempts
grep "Failed password" /var/log/auth.log | wc -l
```

### Change Database Password

```bash
# 1. Connect to PostgreSQL
sudo -u postgres psql

# 2. Change password
ALTER USER farmuser WITH PASSWORD 'new_secure_password';

# 3. Exit
\q

# 4. Update .env file
nano /root/CowsVille-backend/.env
# Change DB_PASSWORD=new_secure_password

# 5. Restart application
systemctl restart cowsville
```

---

## 🚀 Future Enhancements

### Adding SSL/HTTPS (When Domain is Ready)

```bash
# 1. Install Certbot
apt install certbot python3-certbot-nginx

# 2. Obtain SSL certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 3. Update .env
nano /root/CowsVille-backend/.env
# Set SECURE_SSL_REDIRECT=True

# 4. Update productions_settings.py
nano /root/CowsVille-backend/FarmManagerSystem/productions_settings.py
# Set CSRF_COOKIE_SECURE = True
# Set SESSION_COOKIE_SECURE = True

# 5. Restart services
systemctl restart cowsville nginx
```

### Set Up Automated Backups

```bash
# Create backup script
nano /root/backup_script.sh
```

Add this content:

```bash
#!/bin/bash
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
sudo -u postgres pg_dump farmmanager | gzip > $BACKUP_DIR/farmmanager_$DATE.sql.gz

# Keep only last 7 days of backups
find $BACKUP_DIR -name "farmmanager_*.sql.gz" -mtime +7 -delete

echo "Backup completed: farmmanager_$DATE.sql.gz"
```

Make it executable and schedule:

```bash
chmod +x /root/backup_script.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add this line:
0 2 * * * /root/backup_script.sh >> /root/backup.log 2>&1
```

### Add Monitoring (Optional)

```bash
# Install monitoring tools
apt install htop iotop nethogs

# For advanced monitoring, consider:
# - Prometheus + Grafana
# - Datadog
# - New Relic
# - Sentry (for error tracking)
```

---

## 📞 Emergency Contacts & Resources

### Quick Reference

- **Server IP**: 78.47.170.156
- **Server Name**: Alemayehu
- **SSH User**: root
- **Application Path**: `/root/CowsVille-backend`
- **Database Name**: farmmanager
- **Database User**: farmuser

### Important Files

- **Application Code**: `/root/CowsVille-backend/`
- **Environment Config**: `/root/CowsVille-backend/.env`
- **Gunicorn Service**: `/etc/systemd/system/cowsville.service`
- **Nginx Config**: `/etc/nginx/sites-available/cowsville`
- **Application Logs**: `/root/CowsVille-backend/logs/`
- **Nginx Logs**: `/var/log/nginx/`

### Common Commands Cheat Sheet

```bash
# Quick health check
systemctl status cowsville nginx postgresql

# Quick restart
systemctl restart cowsville

# View recent errors
journalctl -u cowsville -n 50 --no-pager

# Deploy update
cd /root/CowsVille-backend && git pull && systemctl restart cowsville

# Database backup
sudo -u postgres pg_dump farmmanager > backup_$(date +%Y%m%d).sql

# Check disk space
df -h

# Check memory
free -h
```

---

## 📝 Maintenance Checklist

### Daily

- [ ] Check application is accessible
- [ ] Review error logs for issues
- [ ] Monitor disk space

### Weekly

- [ ] Create database backup
- [ ] Review system resource usage
- [ ] Check for failed login attempts

### Monthly

- [ ] Update system packages
- [ ] Review and rotate logs
- [ ] Test database restore procedure
- [ ] Review firewall rules

### Quarterly

- [ ] Security audit
- [ ] Performance optimization review
- [ ] Backup strategy review
- [ ] Disaster recovery test

---

**Last Updated**: November 24, 2025  
**Maintained By**: DevOps Team

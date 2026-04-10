# 🚀 TradeMind Deployment Guide

This guide covers deploying TradeMind to production environments.

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Frontend built for production
- [ ] SSL certificates obtained
- [ ] Security headers configured
- [ ] CORS properly restricted
- [ ] Monitoring set up
- [ ] Backups configured

---

## 🌐 Deployment Options

### **Option 1: AWS (Recommended for Production)**

#### Backend (EC2 + RDS)

1. **Launch EC2 Instance**
   ```bash
   # Ubuntu 22.04 LTS, t3.medium or larger
   
   # Connect and update
   ssh -i key.pem ubuntu@your-instance-ip
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install python3.11 python3-pip postgresql-client -y
   ```

2. **Deploy Backend**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/trademind.git
   cd trademind/backend
   
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   nano .env  # Add production values
   
   # Run migrations
   python reset_db.py
   ```

3. **Setup Gunicorn + Nginx**
   ```bash
   # Install Gunicorn
   pip install gunicorn
   
   # Create systemd service
   sudo nano /etc/systemd/system/trademind.service
   ```
   
   ```ini
   [Unit]
   Description=TradeMind FastAPI Application
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/trademind/backend
   Environment="PATH=/home/ubuntu/trademind/backend/venv/bin"
   ExecStart=/home/ubuntu/trademind/backend/venv/bin/gunicorn \
       -w 4 \
       -k uvicorn.workers.UvicornWorker \
       --bind 0.0.0.0:8000 \
       main:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   # Start service
   sudo systemctl daemon-reload
   sudo systemctl enable trademind
   sudo systemctl start trademind
   ```

4. **Setup Nginx Reverse Proxy**
   ```bash
   sudo apt install nginx -y
   sudo nano /etc/nginx/sites-available/trademind
   ```
   
   ```nginx
   upstream trademind_backend {
       server 127.0.0.1:8000;
   }
   
   server {
       listen 80;
       server_name your-domain.com;
   
       # Redirect HTTP to HTTPS
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl http2;
       server_name your-domain.com;
   
       # SSL certificates (use Let's Encrypt)
       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
   
       # Security headers
       add_header Strict-Transport-Security "max-age=31536000" always;
       add_header X-Frame-Options "SAMEORIGIN" always;
       add_header X-Content-Type-Options "nosniff" always;
       add_header X-XSS-Protection "1; mode=block" always;
   
       location / {
           proxy_pass http://trademind_backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/trademind /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Setup RDS Database**
   - Create PostgreSQL instance on AWS RDS
   - Update `DATABASE_URL` in .env with RDS endpoint
   - Ensure security group allows EC2 access
   - Run migrations: `python reset_db.py`

#### Frontend (CloudFront + S3)

1. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Upload to S3**
   ```bash
   # Create S3 bucket
   aws s3 mb s3://your-trademind-frontend
   
   # Upload build files
   aws s3 sync dist/ s3://your-trademind-frontend/ \
       --delete \
       --cache-control "max-age=31536000"
   ```

3. **Setup CloudFront Distribution**
   - Create CloudFront distribution pointing to S3
   - Enable caching for static assets
   - Point domain to CloudFront

---

### **Option 2: Heroku (Quick & Easy)**

#### Backend Deployment
```bash
# Install Heroku CLI
npm install -g heroku

# Login and create app
heroku login
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python reset_db.py
```

#### Frontend Deployment
```bash
# Deploy to Vercel (faster for frontend)
npm install -g vercel
vercel
```

---

### **Option 3: Docker + Docker Compose (Flexible)**

1. **Build Docker Images**
   ```bash
   docker-compose build
   ```

2. **Run Containers**
   ```bash
   docker-compose up -d
   ```

3. **Deploy to Production**
   ```bash
   # Push to Docker Registry
   docker tag trademind-backend:latest yourdocker/trademind-backend:latest
   docker push yourdocker/trademind-backend:latest
   
   # Deploy to Kubernetes, AWS ECS, or Docker Swarm
   ```

---

## 🔒 Security Configuration

### **Environment Variables (Production)**
```env
DEBUG=False
SECRET_KEY=[Generate strong key: openssl rand -hex 32]
DATABASE_URL=postgresql://...  # Use strong password
ALLOWED_ORIGINS=https://your-domain.com
ENVIRONMENT=production
```

### **Database Security**
```sql
-- Create restricted database user
CREATE USER trademind_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE trademind TO trademind_user;
GRANT USAGE ON SCHEMA public TO trademind_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO trademind_user;
```

### **SSL/TLS**
```bash
# Install Let's Encrypt certbot
sudo apt install certbot python3-certbot-nginx -y

# Generate certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renewal (runs daily)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### **Firewall Rules**
```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

---

## 📊 Monitoring & Logging

### **Application Monitoring**

1. **Setup CloudWatch (AWS)**
   ```python
   # In your FastAPI app
   import watchtower
   import logging
   
   logger = logging.getLogger(__name__)
   logger.addHandler(watchtower.CloudWatchLogHandler())
   ```

2. **Error Tracking (Sentry)**
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.fastapi import FastApiIntegration
   
   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[FastApiIntegration()],
       traces_sample_rate=0.1
   )
   ```

3. **Performance Monitoring (New Relic)**
   ```bash
   pip install newrelic
   newrelic-admin run-program uvicorn main:app
   ```

### **Log Aggregation**
```bash
# Setup ELK Stack (Elasticsearch, Logstash, Kibana)
# Or use managed service: DataDog, Splunk, etc.

# Configure Nginx to log
access_log /var/log/nginx/trademind-access.log;
error_log /var/log/nginx/trademind-error.log warn;
```

---

## 🔄 Continuous Deployment (CI/CD)

### **GitHub Actions Workflow**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    # Deploy backend
    - name: Deploy Backend to EC2
      run: |
        ssh -i ${{ secrets.EC2_KEY }} ubuntu@${{ secrets.EC2_HOST }} \
        'cd trademind && git pull origin main && \
        source backend/venv/bin/activate && \
        pip install -r backend/requirements.txt && \
        sudo systemctl restart trademind'
    
    # Deploy frontend
    - name: Deploy Frontend to S3
      run: |
        cd frontend
        npm install
        npm run build
        aws s3 sync dist/ s3://${{ secrets.S3_BUCKET }} --delete
    
    # Invalidate CloudFront
    - name: Invalidate CloudFront
      run: |
        aws cloudfront create-invalidation \
        --distribution-id ${{ secrets.CLOUDFRONT_DIST }} \
        --paths "/*"
```

---

## 📈 Performance Optimization

### **Frontend**
- [ ] Enable gzip compression
- [ ] Minify JavaScript/CSS
- [ ] Lazy load images
- [ ] Use CDN for static assets
- [ ] Cache static files

### **Backend**
- [ ] Use database connection pooling
- [ ] Enable query caching
- [ ] Optimize SQL queries
- [ ] Use Redis for caching
- [ ] Load balance with multiple app instances

### **Database**
- [ ] Add indexes on frequently queried columns
- [ ] Archive old data
- [ ] Regular ANALYZE/VACUUM
- [ ] Monitor slow queries

---

## 🆘 Troubleshooting

### **500 Error on Production**
```bash
# Check application logs
journalctl -u trademind -n 100

# Check Nginx logs
tail -f /var/log/nginx/error.log
```

### **Database Connection Issues**
```bash
# Test connection
psql -h your-rds-endpoint -U postgres -d trademind

# Check connection pool
SELECT * FROM pg_stat_activity;
```

### **High CPU Usage**
- Scale horizontally (add more instances)
- Optimize slow queries
- Increase memory/compute resources

---

## 📝 Backup & Recovery

### **Database Backups**
```bash
# Manual backup
pg_dump -h your-rds-endpoint -U postgres trademind > backup.sql

# Automated backups (AWS RDS)
# Enable automatic backups: 7 day retention
# Create snapshots for long-term storage

# Restore from backup
psql -h new-rds-endpoint -U postgres trademind < backup.sql
```

### **Application Code**
```bash
# Always tag releases
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0

# Keep deployment history
# Use blue-green deployments for zero downtime
```

---

## ✅ Post-Deployment Checklist

- [ ] Health check endpoint responds
- [ ] SSL certificate valid
- [ ] Environment variables configured
- [ ] Database migrations completed
- [ ] Monitoring agents active
- [ ] Backups running
- [ ] Log aggregation working
- [ ] Error tracking operational
- [ ] Performance acceptable
- [ ] Security scan passed

---

## 📞 Support

For deployment issues:
1. Check logs first
2. Review security group rules
3. Verify environment variables
4. Test locally in production mode
5. Contact cloud provider support

**Happy deploying! 🚀**

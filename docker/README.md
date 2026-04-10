      # 🚀 Fintech AI System (Full Stack + ML + Pipeline)

## 🧱 Services

- FastAPI Backend (Auth + Recommendations + ML)
- React Frontend (Dashboard)
- PostgreSQL (Database)
- Redis (Cache + Celery Broker)
- Celery Worker + Scheduler (Data Pipeline)

---

## ⚙️ Setup Instructions

### 1. Clone Repo

git clone <repo_url>
cd project

---

### 2. Setup Environment

cp .env.example .env

---

### 3. Run System

docker-compose up --build

---

## 🌐 Access

Frontend:
http://localhost:3000

Backend API:
http://localhost:8000/docs

---

## 🔁 Pipeline

Celery Worker:
Runs background jobs

Celery Beat:
Runs scheduled stock data pipeline daily

---

## 🧠 ML

- Train model:
docker exec -it backend python ml/train.py

- Predict:
Integrated via backend service

---

## 📦 Features

- Authentication (JWT)
- Stock classification engine
- AI recommendation engine
- LSTM prediction model
- Automated data pipeline
- Fully containerized system

---

## 🛑 Stop System

docker-compose down
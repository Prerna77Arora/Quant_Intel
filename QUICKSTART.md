# ⚡ Quick Start Guide - TradeMind

Get TradeMind running in **5 minutes** ⏱️

---

## 🎯 For the Impatient

### **TL;DR - Copy & Paste Commands**

```bash
# 1. Clone repo
git clone https://github.com/yourusername/trademind.git && cd trademind

# 2. Backend (Terminal 1)
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python reset_db.py
uvicorn main:app --reload

# 3. Frontend (Terminal 2)
cd frontend
npm install
npm run dev
```

Visit: **http://localhost:5173** 🚀

---

## 📝 Step-by-Step Setup

### **Prerequisites Check**
```bash
python --version      # Should be 3.10+
node --version        # Should be 16+
npm --version         # Should be 8+
```

If not installed:
- [Python 3.10+](https://www.python.org/)
- [Node.js 16+](https://nodejs.org/)

---

### **Step 1: Clone & Navigate** (30 seconds)

```bash
git clone https://github.com/yourusername/trademind.git
cd trademind
```

---

### **Step 2: Setup Backend** (2 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python reset_db.py

# Start server
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ Backend is ready at `http://localhost:8000`

---

### **Step 3: Setup Frontend** (2 minutes)

Open a **new terminal** window:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Expected output:**
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
```

✅ Frontend is ready at `http://localhost:5173`

---

### **Step 4: Test the App** (1 minute)

1. Open browser: `http://localhost:5173`
2. Click "Create New Account"
3. Register with any email & password
4. Login with those credentials
5. Explore the dashboard!

---

## 🧪 What Can You Test?

### ✅ Authentication
- Register → Creates user in database
- Login → Returns JWT token, stores in localStorage
- Logout → Clears token

### ✅ Dashboard
- View portfolio overview
- See stock watchlist
- View recent recommendations

### ✅ Stock Analysis
- Search for stocks
- View ML price predictions
- See buy/hold/sell recommendations
- View risk metrics (stop loss, target)

### ✅ Chatbot
- Ask investment questions
- Get AI responses
- Build investment profile

---

## 🐛 Troubleshooting Quick Fixes

### **Backend won't start?**
```bash
# Make sure you're in the backend directory
cd backend

# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Check Python version
python --version

# Reinstall deps
pip install -r requirements.txt --force-reinstall

# Try again
uvicorn main:app --reload
```

### **Frontend won't start?**
```bash
# Make sure you're in the frontend directory
cd frontend

# Clear cache
npm cache clean --force

# Reinstall
npm install

# Clear node_modules and try again
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### **Can't login?**
1. Make sure backend is running (check `http://localhost:8000/docs`)
2. Clear browser cache/localStorage (F12 → Application → Storage)
3. Try registering a new account
4. Check terminal logs for errors

### **"Cannot find module" error?**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

---

## 📂 Project Structure (Simplified)

```
TradeMind/
├── frontend/           # React app → http://localhost:5173
├── backend/            # FastAPI → http://localhost:8000
│   ├── routers/        # API endpoints
│   ├── models/         # Database models
│   └── services/       # Business logic
└── ml/                 # ML models (LSTM predictions)
```

---

## 🔑 Default Test Account

After `reset_db.py`:
- Email: Any email you register with
- Password: Any password ≥ 6 characters

---

## 📚 API Testing (Optional)

Once backend is running:

```bash
# Interactive API docs
http://localhost:8000/docs   # Swagger UI
http://localhost:8000/redoc  # ReDoc

# Example: Get current user
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/auth/me
```

---

## 🚀 Next Steps

1. **Explore the Code**
   - Frontend: `frontend/src/pages/`
   - Backend: `backend/routers/`

2. **View Database**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres -d trademind
   
   # List tables
   \dt
   ```

3. **Check Environment Files**
   ```bash
   # Frontend
   cat frontend/.env.local
   
   # Backend
   cat backend/.env
   ```

4. **Read Full Documentation**
   - [README.md](./README.md) - Complete project overview
   - [API_TESTING_GUIDE.md](./API_TESTING_GUIDE.md) - Detailed API testing
   - [DEPLOYMENT.md](./DEPLOYMENT.md) - Production deployment

---

## 💡 Pro Tips

- **Keep both terminals open** while developing
- **Use `--reload` flag** on backend for auto-restart on file changes
- **Clear browser cache** if you see stale data
- **Check browser console** (F12) for frontend errors
- **Check terminal logs** for backend errors
- **Use Swagger UI** (`http://localhost:8000/docs`) to test APIs
- **Use Redux DevTools** (if needed) to debug state

---

## 🎓 Directory Navigation

```bash
# Go to backend
cd backend

# Go back to root
cd ..

# Go to frontend
cd frontend

# Go back again
cd ..
```

---

## ⏱️ Time Breakdown

| Task | Time |
|------|------|
| Clone repo | 30s |
| Backend setup | 90s |
| Frontend setup | 60s |
| First test | 60s |
| **Total** | **~4 minutes** |

---

## 🎉 You're All Set!

Two servers running. One app working. Ready to impress! 🚀

**Questions?** Check [README.md](./README.md) or open an issue.

---

<div align="center">

### Ready to build? Happy coding! 💻

**TradeMind - Making investing intelligent** ✨

</div>

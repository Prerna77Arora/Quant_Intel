# 🚀 TradeMind - AI-Powered Stock Intelligence Platform

<div align="center">

![TradeMind](https://img.shields.io/badge/TradeMind-FinTech-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-blue?style=for-the-badge)
![React](https://img.shields.io/badge/React-19+-61DAFB?style=for-the-badge&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=for-the-badge&logo=postgresql)
![LSTM](https://img.shields.io/badge/ML-LSTM%20%7C%20PyTorch-orange?style=for-the-badge)

**An intelligent, real-time stock analysis platform powered by machine learning and conversational AI**

[Architecture](#-system-architecture) • [Installation](#-installation--setup) • [API Docs](#-api-endpoints) • [Contributing](#-contributing)

</div>

---

## 📌 Overview

**TradeMind** is a full-stack fintech platform that democratizes stock analysis through AI-powered predictions, personalized recommendations, and intelligent chatbot guidance. Built with modern architecture principles, it combines real-time data processing, machine learning, and a responsive user interface.

### 🎯 Core Features

- 🤖 **AI-Powered Predictions** - LSTM-based time-series forecasting for stock prices
- 💡 **Smart Recommendations** - Buy/Hold/Sell suggestions with confidence scores
- 📊 **Risk Analytics** - Automated stop-loss and target price calculations
- 💬 **Investment Chatbot** - Real-time conversational guidance on investment queries
- 🎨 **Modern Dashboard** - Intuitive UI for portfolio monitoring and analysis
- 🔐 **Secure Authentication** - JWT-based auth with refresh token support
- ⚡ **RESTful APIs** - Production-ready FastAPI backend

---

## 🏗️ System Architecture

### **High-Level Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                             │
│  (React 19 + Vite + TailwindCSS)                                 │
│                                                                    │
│  ┌──────────────┐  ┌──────────┐  ┌─────────────┐  ┌────────────┐│
│  │  Dashboard   │  │ Analysis │  │ Chatbot     │  │  Profile   ││
│  └──────────────┘  └──────────┘  └─────────────┘  └────────────┘│
└───────┬────────────────────────────────────────────────────┬──────┘
        │                                                    │
        │          Context API (Auth) + Axios             │
        │                                                  │
        ├─────────────────────────┬───────────────────────┤
        ▼                         ▼                       ▼
┌───────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                             │
│                    (Nginx Reverse Proxy)                           │
│                                                                    │
│  • JWT Token Validation  • CORS Handling  • Rate Limiting        │
└───────────┬────────────────────────────────────────────┬──────────┘
            │                                            │
            ▼                                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND API LAYER                              │
│              (FastAPI + Uvicorn Server)                          │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │ Auth Router │  │ Stock Router │  │ Prediction Router│       │
│  └─────────────┘  └──────────────┘  └──────────────────┘       │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │ Recommendation │  │ Chatbot Router│  │ User Router     │       │
│  └─────────────┘  └──────────────┘  └──────────────────┘       │
│                                                                  │
│  Request Validation (Pydantic) → Business Logic → Response      │
└────┬────────────────────────────────────────────────────────┬───┘
     │                                                        │
     ▼                                                        ▼
┌──────────────────────┐                          ┌─────────────────┐
│  SERVICE LAYER       │                          │   DATA LAYER    │
│  (Business Logic)    │                          │  (SQLAlchemy)   │
│                      │                          │                 │
│  • auth_service      │                          │  • User Model   │
│  • stock_service     │                          │  • Stock Model  │
│  • prediction_service│ ◄─────────────────────► │  • Rec Model    │
│  • chatbot_service   │                          │  • Chat Model   │
│  • recommendation... │                          │                 │
└──────────────────────┘                          └────────┬────────┘
                                                          │
                                                          ▼
                            ┌─────────────────────────────────────┐
                            │   DATABASE LAYER                    │
                            │  (PostgreSQL via Supabase)          │
                            │                                     │
                            │  • users table                      │
                            │  • stocks table                     │
                            │  • recommendations table            │
                            │  • chatbot_sessions table           │
                            │  • chat_messages table              │
                            └─────────────────────────────────────┘
```

### **Component Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│              ML PIPELINE (Separate Process)                  │
│                                                             │
│  Data Fetcher → Pre-processing → Feature Engineering       │
│       ↓              ↓                  ↓                   │
│  Real-time  →  Normalization   →  Technical Indicators    │
│  Stock Data      & Cleaning         & Patterns             │
│       │              │                  │                   │
│       └──────────────┴──────────────────┘                  │
│              ▼                                              │
│       ┌──────────────────────┐                             │
│       │  LSTM Neural Network │                             │
│       │  (PyTorch Model)     │                             │
│       └──────────────────────┘                             │
│              ▼                                              │
│    Price Predictions & Confidence Scores                   │
│              │                                              │
│              ▼                                              │
│   Store in Backend Database → API Endpoints                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Detailed Architecture Breakdown

### **1. Frontend Layer (React 19 + Vite)**

#### Structure:
```
frontend/src/
├── pages/                    # Route components
│   ├── Login.jsx            # Auth page
│   ├── Register.jsx         # Registration page
│   ├── Dashboard.jsx        # Main dashboard
│   ├── StockAnalysis.jsx    # Stock details & predictions
│   ├── Recommendations.jsx  # AI-generated recommendations
│   ├── Advisor.jsx          # Chatbot interface
│   └── ChatProfile.jsx      # User profile building
│
├── components/              # Reusable UI components
│   ├── Chart.jsx           # Charting library wrapper
│   ├── Loader.jsx          # Loading spinner
│   ├── Navbar.jsx          # Top navigation
│   ├── Sidebar.jsx         # Left sidebar menu
│   ├── StockCard.jsx       # Stock summary card
│   └── Topbar.jsx          # Header section
│
├── hooks/                   # Custom React hooks
│   └── useAuth.jsx         # Global auth context hook
│
├── services/                # API client layer
│   ├── api.js              # Axios instance with interceptors
│   ├── authService.js      # Auth API calls
│   ├── stockService.js     # Stock API calls
│   ├── predictionService.js # Prediction API calls
│   ├── recommendationService.js # Recommendations
│   ├── chatbotService.js   # Chatbot API calls
│   └── pipelineService.js  # Data pipeline calls
│
├── App.jsx                 # Route definitions
├── main.jsx                # Entry with AuthProvider
└── index.css               # Global styles
```

#### Key Technologies:
- **React Router v7** - Client-side routing
- **Context API** - Global state management (authentication)
- **Axios** - HTTP client with JWT interceptors
- **TailwindCSS** - Utility-first styling
- **Vite** - Lightning-fast build tool

#### Authentication Flow:
```
User Input (Email/Password)
    ↓
authService.login() → POST /auth/login
    ↓
Backend validates → JWT tokens returned
    ↓
localStorage.setItem(access_token)
    ↓
Axios interceptor adds: Authorization: Bearer {token}
    ↓
All subsequent requests authenticated
    ↓
Token expires → refresh_token used for renewal
    ↓
User logged out → tokens cleared
```

---

### **2. Backend Layer (FastAPI)**

#### Architecture Pattern: **Layered / Clean Architecture**

```
API Request
    ↓
┌─────────────────────────────────┐
│ Router Layer (routers/*)        │ ← Receives HTTP requests
│                                 │  ← Validates request schema
│                                 │  ← Calls service layer
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ Service Layer (services/*)      │ ← Business logic
│                                 │ ← Data validation
│                                 │ ← Calls database layer
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ Dependency Injection            │ ← Database session
│ (utils/dependencies.py)         │ ← Current user
│                                 │ ← Shared resources
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ Data Access Layer               │ ← SQLAlchemy ORM
│ (models/*, schemas/*)           │ ← Database queries
│                                 │ ← Data persistence
└──────────────┬──────────────────┘
               ↓
         PostgreSQL Database
```

#### Backend Structure:

```
backend/
├── main.py                   # FastAPI app initialization
│                              # CORS middleware
│                              # Exception handlers
│                              # Startup events
│
├── core/
│   ├── config.py            # Settings management (environment-based)
│   ├── database.py          # SQLAlchemy engine, session factory
│   ├── security.py          # Password hashing (bcrypt)
│   │                         # JWT token creation/validation
│   │                         # Token payload encoding
│   └── log_config.py        # Logging configuration
│
├── models/                   # SQLAlchemy ORM Models
│   ├── user.py              # User(id, email, hashed_password, ...)
│   ├── stock.py             # Stock(symbol, price, sector, ...)
│   ├── recommendation.py    # Recommendation(user_id, stock_id, ...)
│   └── chatbot.py           # ChatbotSession, ChatMessage
│
├── schemas/                  # Pydantic Request/Response Models
│   ├── auth.py              # LoginRequest, RegisterRequest, TokenResponse
│   ├── stock.py             # StockRequest, StockResponse
│   ├── recommendation.py    # RecommendationRequest/Response
│   └── chatbot.py           # ChatMessageRequest/Response
│
├── routers/                  # API Endpoints (Route Handlers)
│   ├── auth.py              # POST /auth/register, /auth/login, /auth/me
│   ├── stock.py             # GET /stocks, /stocks/{symbol}
│   ├── prediction.py        # POST /prediction/predict
│   ├── recommendation.py    # GET /recommendations
│   ├── chatbot.py           # POST /chatbot/chat
│   ├── user.py              # PUT /users/profile
│   └── pipeline.py          # POST /pipeline/run_update
│
├── services/                 # Business Logic Layer
│   ├── auth_service.py      # register_user(), authenticate_user()
│   │                         # generate_tokens()
│   ├── stock_service.py     # get_stocks(), get_stock_details()
│   ├── prediction_service.py # get_stock_prediction(), save_prediction()
│   ├── recommendation_service.py # get_recommendations(), create_rec()
│   ├── chatbot_service.py   # process_chat(), get_chat_history()
│   └── user_service.py      # update_profile(), get_user_profile()
│
├── utils/
│   ├── dependencies.py      # Dependency injection (get_db, get_current_user)
│   └── exceptions.py        # Custom exceptions, error handlers
│
└── requirements.txt         # Python dependencies
```

#### Request/Response Flow for Login:

```
POST /auth/login
├── Request: {email, password}
│
├─► Router Layer (auth.py)
│   ├─ Validate schema with Pydantic
│   ├─ Extract database session (Depends(get_db))
│   ├─ Extract current user dependency (optional)
│   └─ Call auth_service.authenticate_user()
│
├─► Service Layer (auth_service.py)
│   ├─ Query database for user by email
│   ├─ Verify password (bcrypt.verify)
│   ├─ Call security.generate_tokens(user_id)
│   └─ Return token dict
│
├─► Data Layer (models/user.py)
│   └─ Execute SQLAlchemy query
│
├─► Database (PostgreSQL)
│   └─ SELECT * FROM users WHERE email = ?
│
└─ Response: {access_token, refresh_token, token_type, expires_in}
```

---

### **3. Data Layer - SQLAlchemy Models**

#### User Model:
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    
    # Investment profile
    risk_tolerance = Column(String)  # low, medium, high
    budget = Column(Float)
    investment_horizon = Column(String)  # short, medium, long
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="user")
    chat_sessions = relationship("ChatbotSession", back_populates="user")
```

#### Stock Model:
```python
class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    name = Column(String)
    price = Column(Float)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(Float)
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="stock")
```

#### Recommendation Model:
```python
class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    
    action = Column(String)  # BUY, HOLD, SELL
    confidence = Column(Float)  # 0.0 to 1.0
    target_price = Column(Float)
    stop_loss = Column(Float)
    allocation_percentage = Column(Float)
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    stock = relationship("Stock", back_populates="recommendations")
```

---

### **4. Machine Learning Pipeline**

#### Process Flow:

```
1. DATA COLLECTION
   ├─ fetcher.py: Fetch real-time stock data from APIs
   ├─ Store in temporary storage
   └─ Trigger at scheduled intervals

2. DATA PREPROCESSING
   ├─ preprocessing.py: Clean & normalize data
   ├─ Handle missing values
   ├─ Remove outliers
   └─ Create time-series sequences

3. FEATURE ENGINEERING
   ├─ features.py: Calculate technical indicators
   │  ├─ Moving averages (20, 50, 200)
   │  ├─ RSI (Relative Strength Index)
   │  ├─ MACD (Moving Average Convergence Divergence)
   │  ├─ Bollinger Bands
   │  └─ Volume ratios
   ├─ Normalize features (0-1 scale)
   └─ Sequence preparation

4. MODEL INFERENCE
   ├─ model.py: Load trained LSTM model
   ├─ predict.py: Generate predictions
   │  ├─ Input: 30 days of historical data
   │  ├─ Output: Future price (1-30 days ahead)
   │  └─ Confidence score (softmax)
   └─ Save predictions to database

5. API ENDPOINT
   ├─ prediction_service.py: Fetch from database
   ├─ Format response
   └─ Return to frontend
```

#### LSTM Model Architecture:

```
Input Layer (30 time steps × features)
    ↓
LSTM Layer 1 (128 units, return_sequences=True)
    ↓
Dropout (0.2)
    ↓
LSTM Layer 2 (64 units, return_sequences=False)
    ↓
Dropout (0.2)
    ↓
Dense Layer 1 (32 units, ReLU activation)
    ↓
Dense Layer 2 (1 unit, Linear activation) → Price Prediction
    ↓
Output: Predicted close price
```

---

### **5. Authentication & Security**

#### JWT Token Structure:

```
Access Token (30 minutes):
{
  "sub": "user_id",
  "role": "user",
  "exp": 1234567890,
  "type": "access"
}

Refresh Token (7 days):
{
  "sub": "user_id",
  "exp": 1234567890,
  "type": "refresh"
}

Both signed with SECRET_KEY using HS256 algorithm
```

#### Request Authentication:

```
Browser Request
    ↓
Authorization Header: Bearer {access_token}
    ↓
Axios Interceptor adds header
    ↓
FastAPI extracts token from header
    ↓
JWT validation (signature + expiry)
    ↓
get_current_user dependency returns User object
    ↓
Protected endpoint receives authenticated user
    ↓
Response with 200 OK or 401 Unauthorized
```

---

### **6. Data Flow Examples**

#### Example 1: Stock Prediction Request

```
User clicks "Analyze AAPL"
    ↓
Frontend: GET /stocks/AAPL (with auth token)
    ↓
Backend Router:
    ├─ Validate token → get_current_user
    ├─ Query database for stock predictions
    └─ Return latest prediction
    ↓
Frontend receives:
    {
      "symbol": "AAPL",
      "current_price": 150.25,
      "predicted_price": 165.80,
      "confidence": 0.87,
      "recommendation": "BUY"
    }
    ↓
Frontend renders chart + metrics
    ↓
User sees prediction
```

#### Example 2: Chatbot Conversation

```
User: "Should I buy Tesla stocks?"
    ↓
Frontend: POST /chatbot/chat
    {
      "message": "Should I buy Tesla stocks?",
      "session_id": "xyz"
    }
    ↓
Backend:
    ├─ Fetch chat history from database
    ├─ Get latest TSLA prediction data
    ├─ Pass to chatbot_service
    ├─ Generate response using Recommendation data
    └─ Save conversation to database
    ↓
Response:
    {
      "response": "Based on current metrics...",
      "sentiment": 0.75,
      "related_data": {...}
    }
    ↓
Frontend displays response
```

---

## 📂 File Organization Summary

```
TradeMind/
│
├── frontend/                 # React App
│   ├── src/
│   │   ├── pages/           # Route pages
│   │   ├── components/      # Reusable components
│   │   ├── hooks/           # Custom hooks
│   │   └── services/        # API client services
│   └── package.json
│
├── backend/                 # FastAPI App
│   ├── main.py              # Entry point
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   ├── models/              # Database ORM
│   ├── schemas/             # Data validation
│   ├── core/                # Config & security
│   └── requirements.txt
│
├── ml/                      # Machine Learning
│   ├── model.py             # LSTM architecture
│   ├── train.py             # Training script
│   ├── predict.py           # Inference
│   ├── features.py          # Feature engineering
│   └── models/              # Saved models
│
├── data_pipeline/           # ETL Process
│   ├── fetcher.py          # Data collection
│   ├── preprocessing.py    # Data cleaning
│   ├── scheduler.py        # Task scheduling
│   └── run_pipeline.py     # Pipeline orchestration
│
└── README.md, docs/        # Documentation
```

---

## 🔐 Security Architecture

### **Authentication & Authorization**
- JWT tokens stored in browser localStorage
- Tokens attached to every protected request via Axios interceptor
- Backend validates token signature & expiry
- Refresh token mechanism for token renewal

### **Data Protection**
- Passwords hashed with bcrypt (cost=12)
- Sensitive endpoints require authentication
- CORS restricted to frontend domain
- SQL injection prevention via SQLAlchemy ORM

### **API Security**
```python
@router.get("/recommendations")
def get_recommendations(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user)  # ← Auth required
):
    # Only returns recommendations for current user
    return db.query(Recommendation)\
        .filter(Recommendation.user_id == current_user.id)\
        .offset(skip).limit(limit).all()
```

---

## ⚙️ Installation & Setup

### **Prerequisites**
- Python 3.10+ (backend)
- Node.js 16+ (frontend)
- PostgreSQL 12+ (database)

### **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python reset_db.py
uvicorn main:app --reload
```

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

---

## 🚀 API Endpoints

### **Authentication**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create new account |
| POST | `/auth/login` | Login & get JWT |
| POST | `/auth/logout` | Logout |
| GET | `/auth/me` | Get current user |

### **Stocks**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stocks` | List all stocks |
| GET | `/stocks/{symbol}` | Get stock details |

### **Predictions**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prediction/{symbol}` | Get price prediction |
| POST | `/prediction/predict` | Create new prediction |

### **Recommendations**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommendations` | List user recommendations |
| POST | `/recommendations` | Create recommendation |

### **Chatbot**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chatbot/chat` | Send chat message |
| GET | `/chatbot/session` | Get chat history |

---



**Features shown:**
- 📊 Portfolio performance metrics (Total Investment, Total Profit, Unrealized Loss)
- 📈 AI Risk Score assessment
- 💹 Portfolio performance chart with multiple timeframes (1D, 1W, 1M, 1Y)
- 👁️ Watchlist with real-time ticker information
- ✨ Personalized greeting with profile status

---

### **4. Stock Analysis Page**
*AI-powered detailed stock analysis with predictions*

![Stock Analysis](Images/stock-analysis.png)

**Features shown:**
- 🤖 AI Confidence Score (82% for shown example)
- 💰 Current stock price with daily change
- 📊 Key metrics (Market Cap, P/E Ratio, 52W High/Low)
- 🎯 AI Prediction Signal (BUY/SELL/HOLD with justification)
- 📉 Technical analysis summary
- 🔔 AI Signal alerts

---

### **5. AI Investment Chatbot**
*Real-time conversational investment guidance*

![AI Chatbot](Images/chatbot.png)

**Features shown:**
- 💬 Natural language conversation interface
- 🤖 AI Assistant with investment expertise
- 📊 Context-aware responses based on portfolio
- 💡 Quick action suggestions (Buy stock, Portfolio risk, Today's picks)
- 📈 Integrated data visualization
- ⚡ Real-time response generation

---

### **6. Database - Stock Data Management**
*Real-time stock data stored in PostgreSQL via Supabase*

![Stock Data](Images/stock-data-table.png)

**Tables shown:**
- OHLC data (Open, High, Low, Close prices)
- Multiple stocks tracked (AAPL, MSFT, etc.)
- Time-series data for ML predictions
- Real-time data feed

---

### **7. Database - User Management**
*Secure user authentication and profile storage*

![Users Table](Images/users-table.png)

**Data stored:**
- User email authentication
- Bcrypt hashed passwords
- User roles (user, admin)
- Investment preferences
- Risk profile data

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# API testing (interactive)
http://localhost:8000/docs  # Swagger UI
```

---

## 📈 Performance Optimization

- **Frontend**: Lazy loading, code splitting, image optimization
- **Backend**: Database indexing, query optimization, caching
- **ML**: Batch prediction, model quantization
- **Infrastructure**: CDN for static assets, connection pooling

---

## 🎯 Future Enhancements

- [ ] Real-time WebSocket updates for stock prices
- [ ] Advanced ML models (Transformer-based)
- [ ] Mobile app (React Native)
- [ ] Portfolio optimization engine
- [ ] Paper trading simulator
- [ ] Real brokerage integration

---

## 📄 License

MIT License - See LICENSE file

---

## 👩‍💻 Author

**Prerna Dcreuet** - Full-Stack Developer & AI Engineer
- 📧 prerna7788arora@gmail.com
- 🔗 [GitHub](https://github.com)

---

<div align="center">

**Built with ❤️ for smarter investing**

⭐ If TradeMind helped you, consider giving it a star!

</div>

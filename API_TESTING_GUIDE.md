# TradeMind API Testing Guide

Complete API testing guide with curl examples and expected responses.

---

## 🔧 Setup

Before testing, ensure:
- Backend is running on `http://localhost:8000`
- Database is configured with valid `POSTGRES_URL`
- Frontend is running (if testing full flow)

Store the auth token for subsequent requests:
```bash
export TOKEN="your_access_token_here"
```

---

## 📝 Authentication Endpoints

### 1. Register New User

**Request:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "testuser@example.com",
    "role": "user"
  },
  "message": "Registration successful"
}
```

**Error Response (400):**
```json
{
  "detail": "Email already exists"
}
```

---

### 2. Login

**Request:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "testuser@example.com",
      "role": "user"
    }
  },
  "message": "Login successful"
}
```

**Store token:**
```bash
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

### 3. Get Current User

**Request:**
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "testuser@example.com",
    "role": "user",
    "risk_tolerance": "medium",
    "budget": null,
    "investment_horizon": null,
    "experience_level": "beginner",
    "profile_complete": false
  }
}
```

---

### 4. Logout

**Request:**
```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logout successful. Please clear your local storage."
}
```

---

## 👤 User Endpoints

### 1. Get User Profile

**Request:**
```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "testuser@example.com",
    "role": "user",
    "risk_level": "medium",
    "investment_horizon": null,
    "budget": null
  }
}
```

---

### 2. Update User Profile

**Request:**
```bash
curl -X PUT http://localhost:8000/users/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "risk_level": "high",
    "budget": 100000,
    "investment_horizon": "long-term"
  }'
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "testuser@example.com",
    "role": "user",
    "risk_level": "high",
    "investment_horizon": "long-term",
    "budget": 100000
  }
}
```

---

## 💬 Chatbot Endpoints

### 1. Start Chatbot Session

**Request:**
```bash
curl -X POST http://localhost:8000/chatbot/start \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200) - New Session:**
```json
{
  "success": true,
  "message": "Chatbot session started",
  "data": {
    "session_id": 1,
    "user_id": 1,
    "current_step": 0,
    "total_steps": 5,
    "question": "What is your risk tolerance for investments?",
    "options": ["Low (Conservative)", "Medium (Balanced)", "High (Aggressive)"],
    "message": "Question 1 of 5"
  }
}
```

**Response (200) - Already Complete:**
```json
{
  "success": true,
  "message": "Your profile is already complete!",
  "completed": true,
  "data": {
    "user_id": 1,
    "profile_complete": true
  }
}
```

---

### 2. Process Chatbot Step

**Step 0 - Risk Tolerance:**
```bash
export SESSION_ID="1"

curl -X POST http://localhost:8000/chatbot/step/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 0,
    "response": "High (Aggressive)"
  }'
```

**Response (200):**
```json
{
  "success": true,
  "message": "Great! Moving to the next question.",
  "completed": false,
  "current_step": 1,
  "next_question": {
    "step": 1,
    "question": "What is your investment budget? (Enter amount)",
    "options": ["Custom amount"],
    "message": "Question 2 of 5"
  }
}
```

**Step 1 - Budget:**
```bash
curl -X POST http://localhost:8000/chatbot/step/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 1,
    "response": "500000"
  }'
```

**Response (200):**
```json
{
  "success": true,
  "message": "Great! Moving to the next question.",
  "completed": false,
  "current_step": 2,
  "next_question": {
    "question": "What is your investment horizon?",
    "options": ["Short-term (0-1 year)", "Medium-term (1-5 years)", "Long-term (5+ years)"],
    "message": "Question 3 of 5"
  }
}
```

**Step 2 - Investment Horizon:**
```bash
curl -X POST http://localhost:8000/chatbot/step/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 2,
    "response": "Long-term (5+ years)"
  }'
```

**Step 3 - Experience Level:**
```bash
curl -X POST http://localhost:8000/chatbot/step/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 3,
    "response": "Intermediate"
  }'
```

**Step 4 - Preferred Sectors:**
```bash
curl -X POST http://localhost:8000/chatbot/step/$SESSION_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 4,
    "response": "Technology, Healthcare, Finance"
  }'
```

**Final Response (200):**
```json
{
  "success": true,
  "message": "Profile setup complete! We'll now provide personalized recommendations.",
  "completed": true,
  "current_step": 5
}
```

---

### 3. Get Chatbot Status

**Request:**
```bash
curl -X GET "http://localhost:8000/chatbot/status/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "session_id": 1,
    "current_step": 5,
    "total_steps": 5,
    "completed": true,
    "question": "Profile setup complete!",
    "options": [],
    "message": ""
  }
}
```

---

## 📈 Stock Endpoints

### 1. List All Stocks

**Request:**
```bash
curl -X GET http://localhost:8000/stocks/ \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "symbol": "AAPL",
      "sector": "Technology",
      "industry": "Consumer Electronics",
      "market_cap": 3000000000000,
      "style": "Growth",
      "risk_level": "medium"
    },
    {
      "id": 2,
      "symbol": "MSFT",
      "sector": "Technology",
      "industry": "Software",
      "market_cap": 2500000000000,
      "style": "Growth",
      "risk_level": "medium"
    }
  ]
}
```

---

### 2. Add Stock

**Request:**
```bash
curl -X POST http://localhost:8000/stocks/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "GOOGL",
    "sector": "Technology",
    "industry": "Internet Services",
    "market_cap": 1800000000000,
    "style": "Growth",
    "risk_level": "medium"
  }'
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 3,
    "symbol": "GOOGL",
    "sector": "Technology",
    "industry": "Internet Services",
    "market_cap": 1800000000000,
    "style": "Growth",
    "risk_level": "medium"
  }
}
```

---

### 3. Search Stock (Auto-Fetch If Missing)

**Request - Stock Exists:**
```bash
curl -X GET "http://localhost:8000/stocks/search/AAPL" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "found": true,
  "auto_fetched": false,
  "data": {
    "id": 1,
    "symbol": "AAPL",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "market_cap": 3000000000000,
    "style": "Growth",
    "risk_level": "medium"
  }
}
```

**Request - Stock Not Found (Auto-Fetch Triggered):**
```bash
curl -X GET "http://localhost:8000/stocks/search/TSLA" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200) - Auto-Fetched:**
```json
{
  "success": true,
  "found": true,
  "auto_fetched": true,
  "message": "Stock TSLA was not in database. Auto-fetched and stored.",
  "data": {
    "id": 4,
    "symbol": "TSLA",
    "sector": "Automotive",
    "industry": "Electric Vehicles",
    "market_cap": 800000000000,
    "style": "Growth",
    "risk_level": "high"
  }
}
```

---

## 💡 Recommendation Endpoints

### Get Personalized Recommendations

**Request:**
```bash
curl -X POST http://localhost:8000/recommendations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "risk_level": null
  }'
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "stock_id": 1,
      "action": "Buy",
      "confidence": 0.88,
      "predicted_trend": "Uptrend",
      "stop_loss": 0.85,
      "take_profit": 1.25,
      "allocation": 14.4,
      "reason": "ML prediction: +0.125. AAPL (Technology) aligns with high-risk portfolio.",
      "risk_explanation": "Aggressive strategy - includes high-risk/high-reward opportunities. Prepared for volatility.",
      "strategy": "Growth-focused with calculated risk"
    },
    {
      "id": 2,
      "stock_id": 2,
      "action": "Hold",
      "confidence": 0.75,
      "predicted_trend": "Neutral",
      "stop_loss": 0.85,
      "take_profit": 1.25,
      "allocation": 0,
      "reason": "ML prediction: +0.005. MSFT (Technology) neutral signal.",
      "risk_explanation": "Aggressive strategy - includes high-risk/high-reward opportunities.",
      "strategy": "Growth-focused with calculated risk"
    }
  ]
}
```

---

## 🔄 Pipeline Endpoints

### Refresh All Data

**Request:**
```bash
curl -X POST http://localhost:8000/pipeline/run \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "status": "success",
    "message": "Data refreshed for all stocks",
    "results": [
      {
        "symbol": "AAPL",
        "status": "success"
      },
      {
        "symbol": "MSFT",
        "status": "success"
      },
      {
        "symbol": "GOOGL",
        "status": "success"
      }
    ]
  }
}
```

**Error Response (500):**
```json
{
  "detail": "Pipeline error: connection timeout"
}
```

---

## 🤖 Prediction Endpoints

### Get Stock Prediction

**Request:**
```bash
curl -X GET "http://localhost:8000/prediction/AAPL" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "predicted_price": 0.125,
    "trend": "Uptrend",
    "confidence": 0.85,
    "timestamp": "2024-04-09T12:30:00Z"
  }
}
```

---

## ❌ Common Error Responses

### 401 - Unauthorized (Missing Token)
```bash
curl -X GET http://localhost:8000/stocks/
```

**Response (401):**
```json
{
  "detail": "Not authenticated"
}
```

---

### 401 - Invalid Token
```bash
curl -X GET http://localhost:8000/stocks/ \
  -H "Authorization: Bearer invalid_token"
```

**Response (401):**
```json
{
  "detail": "Invalid token"
}
```

---

### 400 - Bad Request
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid-email",
    "password": ""
  }'
```

**Response (422):**
```json
{
  "detail": [
    {
      "type": "value_error.email",
      "loc": ["body", "email"],
      "msg": "invalid email format"
    }
  ]
}
```

---

### 404 - Not Found
```bash
curl -X GET "http://localhost:8000/stocks/999" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (404):**
```json
{
  "detail": "Stock not found"
}
```

---

## 🧪 Complete User Flow Test

Run these commands in order to test the complete user journey:

```bash
# 1. Register
REGISTER=$(curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "flowtest@example.com",
    "password": "TestPassword123"
  }')
echo "1. Register: $REGISTER"

# 2. Login
LOGIN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "flowtest@example.com",
    "password": "TestPassword123"
  }')
TOKEN=$(echo $LOGIN | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "2. Login Token: $TOKEN"

# 3. Start Chatbot
CHAT_START=$(curl -s -X POST http://localhost:8000/chatbot/start \
  -H "Authorization: Bearer $TOKEN")
SESSION_ID=$(echo $CHAT_START | grep -o '"session_id":[0-9]*' | cut -d':' -f2)
echo "3. Chatbot Session: $SESSION_ID"

# 4. Complete Chatbot Steps
curl -s -X POST "http://localhost:8000/chatbot/step/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"step": 0, "response": "High"}'

curl -s -X POST "http://localhost:8000/chatbot/step/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"step": 1, "response": "100000"}'

curl -s -X POST "http://localhost:8000/chatbot/step/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"step": 2, "response": "Long-term"}'

curl -s -X POST "http://localhost:8000/chatbot/step/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"step": 3, "response": "Intermediate"}'

FINAL=$(curl -s -X POST "http://localhost:8000/chatbot/step/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"step": 4, "response": "Technology,Finance"}')
echo "4. Profile Complete: $FINAL"

# 5. Get Stocks
STOCKS=$(curl -s -X GET http://localhost:8000/stocks/ \
  -H "Authorization: Bearer $TOKEN")
echo "5. Stocks: $STOCKS"

# 6. Get Recommendations
RECS=$(curl -s -X POST http://localhost:8000/recommendations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"risk_level": null}')
echo "6. Recommendations: $RECS"

# 7. Refresh Data
REFRESH=$(curl -s -X POST http://localhost:8000/pipeline/run \
  -H "Authorization: Bearer $TOKEN")
echo "7. Pipeline Refresh: $REFRESH"

# 8. Logout
LOGOUT=$(curl -s -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN")
echo "8. Logout: $LOGOUT"
```

---

## 📊 Response Time Benchmarks

Expected response times (on modern hardware):
- Auth endpoints: < 200ms
- User endpoints: < 100ms
- Stock endpoints: < 150ms
- Chatbot endpoints: < 100ms
- Recommendation generation: < 500ms (depends on # stocks)
- Pipeline refresh: 2-10s (depends on # stocks)

---

## 💾 Sample Test Data

### Create Sample Stocks
```bash
for symbol in AAPL MSFT GOOGL TSLA AMZN; do
  curl -X POST http://localhost:8000/stocks/ \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"symbol\": \"$symbol\",
      \"sector\": \"Technology\",
      \"industry\": \"Tech\",
      \"market_cap\": 1000000000000,
      \"style\": \"Growth\",
      \"risk_level\": \"medium\"
    }"
done
```

---

## 🔍 Debugging Tips

1. **Check Backend Logs:**
   - Look for error messages in terminal where backend is running
   - Check for database connection errors
   - Verify environment variables are loaded

2. **Verify Token:**
   ```bash
   echo $TOKEN
   # Should be a long JWT string starting with eyJ
   ```

3. **Check Database:**
   ```bash
   # Connect to PostgreSQL directly
   psql $POSTGRES_URL -c "SELECT * FROM users LIMIT 1;"
   ```

4. **Test Database Connection:**
   By making an auth request - if DB is not connected, you'll get an error

5. **Review API Documentation:**
   Visit `http://localhost:8000/docs` for interactive Swagger docs

---

**Last Updated:** April 2026

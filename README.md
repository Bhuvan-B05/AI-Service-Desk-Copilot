# 🤖 AI Service Desk Copilot

An AI-powered IT Service Desk application that helps organizations streamline ticket management using Large Language Models (LLMs). Users can create support tickets, receive AI-generated analysis, track ticket status, and manage requests through a modern web interface.

---

## 🌐 Live Demo

**Frontend:** https://ai-service-desk-copilot-frontend.onrender.com/

**Backend API:** https://ai-service-desk-copilot.onrender.com/

**Swagger Documentation:** https://ai-service-desk-copilot.onrender.com/docs

---

## 📌 Features

- 🔐 JWT Authentication (Register & Login)
- 🎫 Create, Update and Delete Support Tickets
- 🤖 AI-powered Ticket Analysis
- 📊 Dashboard Analytics
- 🔎 Search Tickets
- 🎯 Filter by Status and Priority
- 📅 Sort by Creation Date
- 👨‍💻 Protected API Endpoints
- 🗄️ PostgreSQL Database
- ☁️ Production Deployment on Render
- 🐘 Supabase PostgreSQL Integration

---

## 🧠 AI Ticket Analysis

The application uses OpenRouter AI to automatically generate:

- Category
- Priority
- Severity
- Summary
- Root Cause
- Resolution Steps
- Assigned Team
- Estimated Resolution Time

---

## 🛠 Tech Stack

### Frontend

- React
- Vite
- Axios
- CSS

### Backend

- FastAPI
- SQLAlchemy
- JWT Authentication
- OpenRouter AI API

### Database

- PostgreSQL (Supabase)

### Deployment

- Render
- Supabase

---

## 📁 Project Structure

```
AI-Service-Desk-Copilot
│
├── backend
│   ├── ai.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/Bhuvan-B05/AI-Service-Desk-Copilot.git

cd AI-Service-Desk-Copilot
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## 🔑 Environment Variables

### Backend (.env)

```
DATABASE_URL=

SECRET_KEY=

OPENROUTER_API_KEY=

AI_MODEL=
```

### Frontend (.env)

```
VITE_API_URL=
```

---

## 📷 Screenshots

Coming Soon

- Login Page
- Dashboard
- Ticket Creation
- AI Analysis

---

## 📈 Future Improvements

- Email Notifications
- Admin Dashboard
- Ticket Assignment
- File Attachments
- AI Chat Assistant
- Audit Logs

---

## 👨‍💻 Author

**Bhuvan**

GitHub:
https://github.com/Bhuvan-B05

---

## ⭐ If you like this project

Give the repository a ⭐ on GitHub.
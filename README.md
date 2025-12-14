# FastAPI AI Chat Platform

A full-stack **AI-powered chat application** built with **FastAPI** and **React**, focusing on real-world backend architecture, security, scalability, and clean code practices.

This project demonstrates advanced backend concepts such as authentication, real-time communication, rate limiting, AI integrations, and full test coverage.

---

## ✨ Key Features

### 🔐 Authentication & Security

* User **signup & signin** using **JWT-based authentication**
* Secure password hashing with **Argon2**
* **Google reCAPTCHA** validation on both frontend and backend
* CORS configuration to safely connect frontend and backend

### 🤖 AI Chat System

* Multiple AI providers with a unified interface:

  * **Google Gemini**
  * **Groq**
  * **OpenAI** (code implemented, currently disabled due to API key limitations)
* Clean abstraction layer for AI providers using a base AI interface
* System prompt support via markdown file

### ⚡ Real-Time Chat

* **WebSocket-based real-time chat**
* Chat stays synchronized across multiple browser tabs without refreshing
* Persistent chat history stored in the database

### 🚦 Rate Limiting

* Request rate limiting using **FastAPI-Limiter**
* **Redis** used as the rate-limiting backend
* Protects AI endpoints from abuse

### 🗄️ Database & Migrations

* Database modeling using **SQLModel**
* Data validation using **Pydantic**
* Database migrations handled with **Alembic**
* PostgreSQL as the main database

### 🧱 Clean Architecture

* Repository pattern for separating business logic from API layers
* Modular project structure
* Clear separation of concerns (API, models, schemas, repositories, core utilities)

### 🧪 Testing

* Comprehensive test suite using **pytest**
* Unit tests and integration tests
* Async testing support with `pytest-asyncio`

### 🎨 Frontend

* Built with **React + Tailwind CSS**
* Generated and customized using **Lovable**
* Communicates with backend via REST APIs .

---

## 🏗️ Project Structure

```
fastapi-ai/
├── backend/
│   ├── alembic/
│   ├── src/
│   │   ├── ai/                 # AI providers (Gemini, Groq, OpenAI)
│   │   ├── api/                # API routes (auth, chat)
│   │   ├── core/               # Config, auth, security, helpers
│   │   ├── models/             # Database models
│   │   ├── prompts/            # System prompts
│   │   ├── repositories/       # Data access layer
│   │   ├── schemas/            # Pydantic schemas
│   │   └── tests/              # Unit & integration tests
│   ├── main.py
│   ├── alembic.ini
│   ├── .env
│   └── .env.example
├── frontend/                   # React + Tailwind frontend
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

### Backend

* **FastAPI**
* **SQLModel & SQLAlchemy**
* **PostgreSQL**
* **Alembic**
* **Redis**
* **JWT Authentication**
* **WebSockets**
* **FastAPI-Limiter**
* **Pytest**

### AI Integrations

* Google Gemini
* Groq
* OpenAI (optional / disabled)

### Frontend

* React
* Tailwind CSS

---

## 🚀 Setup & Run

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Run Tests

```bash
pytest
```

---

## 📌 Notes

* Redis must be running for rate limiting
* OpenAI integration is implemented but disabled by default
* Environment variables are documented in `.env.example`

---

## 📄 License

This project is for learning and portfolio purposes.

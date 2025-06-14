# 💸 Etracker — Expense Tracker App (Django + React)

A simple full-stack Expense Tracker built with **Django REST Framework** (backend) and **React** (frontend). Authenticated users can log, view, and categorize expenses. Admins have extended access and analytics.

---

## 🚀 Features

- User Registration/Login using **Session Authentication**
- CSRF Protection (Secure for React frontend)
- Track expenses with fields like title, amount, category, date, notes
- Admin access to all users' expenses
- Filtering by category and date range
- Summary endpoint for total expenses by category

---

## 📦 Backend (Django) Setup

### ✅ Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)

---

### 🛠️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/vishnudas-max/Etracker.git
cd Etracker

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a `.env` file in the root backend directory
# .env.example

# CORS settings — comma-separated list of allowed origins (frontend URLs)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# CSRF trusted origins — comma-separated list (same as frontend URLs)
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Enable sending credentials (cookies, sessions)
CORS_ALLOW_CREDENTIALS=True

# 5. Make and apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver

```
You can find the forntend here https://github.com/vishnudas-max/Etracker_frontend.git

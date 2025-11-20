# 🍽️ Meal Planner & Recipe Manager

A **full-featured Django-based Meal Planning and Recipe Management Web Application** that helps users organize their cooking, plan weekly meals, and manage shopping lists — all in one place.

A clean, modern, recruiter-friendly project showcasing **Django**, **DRF**, **Allauth**, **PostgreSQL**, **AWS S3**, and a production-ready backend structure.

---

## ✨ Features

### 📖 Recipe Management

* Create, edit, and share recipes with rich media (images & videos)
* Categorize recipes by cuisine (Italian, Mexican, Asian, etc.)
* Add dietary tags (Vegan, Keto, Gluten-Free, etc.)
* Track difficulty level and cooking time
* Automatic nutrition breakdown per serving (calories, protein, carbs, fats)
* Recipe rating & commenting system
* Public / Private recipe visibility

---

### 📅 Meal Planning

* Create **weekly meal plans** with flexible date ranges
* Plan meals by **day** and **meal type** (breakfast, lunch, dinner, snacks)
* Adjust serving sizes for each meal
* Track active and historical plans
* Link recipes directly into meal slots

---

### 🛒 Shopping Lists

* Auto-generate shopping lists from selected meal plans
* Items grouped by category for easy navigation
* Checkbox tracking for purchased items
* Add custom items manually
* Share shopping lists with other users
* One-click ingredient compilation from recipes

---

### 👤 User Management

* User authentication using **Django Allauth**
* Email login + social authentication ready
* User profile with personal recipe collections

---

### 🔌 RESTful API

Built fully using **Django REST Framework**:

* Token-based authentication
* Endpoints for recipes, meal plans & shopping lists
* Pagination, filtering & search
* Auto-generated API docs using **Swagger (drf-yasg)**

---

## 🛠️ Tech Stack

| Component         | Technology                       |
| ----------------- | -------------------------------- |
| Backend           | **Django 5.0**                   |
| API               | **Django REST Framework**        |
| Auth              | **Django Allauth**               |
| Database          | SQLite (dev) → PostgreSQL (prod) |
| Storage           | AWS S3 via Django Storages       |
| Static Files      | WhiteNoise                       |
| API Docs          | drf-yasg (Swagger UI)            |
| Production Server | Gunicorn                         |

---

## 🚀 Getting Started

### 1️⃣ Clone the Project

```bash
https://github.com/yourusername/meal-planner.git
cd meal-planner
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate    # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Start Server

```bash
python manage.py runserver
```

Your app is live at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📚 API Documentation

Swagger UI auto-generated:

```
/api/docs/
```

---

## 📦 Project Structure

```
meal_planner/
│
├── recipes/          # Recipe module
├── mealplans/        # Meal planning module
├── shopping/         # Shopping list module
├── accounts/         # Authentication and user profiles
├── api/              # DRF API endpoints
└── templates/        # HTML templates (if needed)
```

---

## 🌐 Deployment Ready

* WhiteNoise for static files
* Gunicorn for production server
* PostgreSQL-ready config
* AWS S3 for media storage

---

## ❤️ Why This Project Stands Out

✔ Production-level structure
✔ Clean API architecture
✔ Recruiter-friendly & scalable
✔ Real-world use case
✔ Modern tech stack

---

## 🧑‍💻 Author

**Yash Goyal**
Full Stack Developer | Django | React | AI & Blockchain Enthusiast

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

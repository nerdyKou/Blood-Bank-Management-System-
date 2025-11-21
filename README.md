# 🩸 Blood Bank Management System

A secure and scalable **Django-based web application** designed to manage **blood donors, blood inventory, and blood requests** efficiently.

## 🚀 Features
- Staff authentication (login/logout)
- Donor management with auto-inventory update
- Blood inventory management
- Blood request processing
- Admin dashboard
- Fully responsive UI (Bootstrap)

## 🛠 Tech Stack
- Python 3
- Django
- HTML, CSS, Bootstrap
- SQLite

## 📂 Project Structure
```
blood-bank-management-system/
├── bank/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/bank/
├── blood_bank/
│   ├── settings.py
│   ├── urls.py
├── db.sqlite3
├── manage.py
└── README.md
```

## ⚙️ Installation
```bash
git clone https://github.com/yourusername/blood-bank-management-system.git
cd blood-bank-management-system
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## ▶️ Run the Project
Visit:
- http://127.0.0.1:8000/ (Dashboard)
- http://127.0.0.1:8000/admin/ (Admin panel)



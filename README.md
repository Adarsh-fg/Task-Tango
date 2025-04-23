# ✅ Advanced Flask To-Do List App

This is a feature-rich **To-Do List web application** built with **Flask**, supporting user authentication, task tracking, priority setting, due dates, sorting, analytics, and more. 

## 🛠️ Features

- 🧑‍💼 User registration and login with secure password hashing
- 📋 Add, delete, and complete tasks
- 🗓 Set **due dates** and assign **priority levels**
- 🔄 Sort tasks by priority, due date, or completion status
- 📊 View task analytics (completed, pending, priority breakdown)
- 🔐 User authentication with session management using Flask-Login
- 🚀 Responsive UI with Bootstrap templates

## 📁 Project Structure

```
flask-todo-app/
│
├── templates/               # HTML templates
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   └── analytics.html
│
├── static/                  # Static files (CSS/JS)
│
├── forms.py                 # Flask-WTF Forms for Task, Login, Register
├── app.py                   # Main Flask app
├── tasks.db                 # SQLite database (auto-generated)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## 🧪 Tech Stack

- **Flask** (Web Framework)
- **Flask-WTF** (Form validation)
- **Flask-Login** (User sessions)
- **Flask-Migrate** (Database migrations)
- **SQLite** (Lightweight database)
- **SQLAlchemy** (ORM)
- **WTForms** (Form fields & validation)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/flask-todo-app.git
cd flask-todo-app
```

### 2. Set Up Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python app.py
```

The app will run on `http://localhost:5000`.

---

## ✅ How It Works

### Authentication
- Secure password hashing using Werkzeug
- Login/Logout using `Flask-Login`

### Task Management
- Add task with title, priority (Low/Medium/High), and optional due date
- Toggle task completion
- Delete tasks securely
- User-specific task storage

### Analytics
- Shows total, completed, and pending tasks
- Priority distribution

### Sorting
- Dropdown filter for:
  - Priority (High → Low)
  - Due Date (Earliest first)
  - Completion status

---

## 📋 Sample `.env` or Configuration

No environment file needed — `SECRET_KEY` and DB URI are configured in `app.py`.

---

## 📦 requirements.txt

```txt
Flask==2.3.2
Flask-Login==0.6.3
Flask-WTF==1.1.1
WTForms==3.1.2
Flask-SQLAlchemy==3.1.1
Werkzeug==2.3.7
Flask-Migrate==4.0.5
```

---

## 📬 Contact

For questions or collaboration:
- GitHub: [Adarsh-fg](https://github.com/Adarsh-fg)
- Email: adarshai5770@gmail.com
---

**Happy tasking! 📝✨**

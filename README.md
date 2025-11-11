# 🎯 Smart Automated Bidding System

A production-ready Django auction platform with an intelligent bot that simulates realistic bidding behavior across three strategic phases.

## 📋 Table of Contents

1. [Features](#-features)
2. [Prerequisites](#-prerequisites)
3. [Quick Start](#-quick-start)
4. [Project Structure](#-project-structure)
5. [How to Use](#-how-to-use)
6. [Deployment](#-deployment)
7. [Bot Strategy](#-bot-strategy)
8. [Documentation](#-documentation)

---

## ✨ Features

### Core Features
- **🎯 Phase-Based Bot Strategy**: Intelligent bot adapts bidding behavior across 3 distinct phases
- **💻 Beautiful Web Interface**: Modern, responsive UI built with Bootstrap 5
- **🔌 RESTful API**: Complete REST API with Swagger/OpenAPI documentation
- **🔄 Real-time Updates**: Polling-based updates (simple and reliable)
- **🔐 User Authentication**: Token and session-based authentication
- **📊 Analytics Dashboard**: Statistics and insights on auctions
- **🗄️ Database Support**: SQLite for development, PostgreSQL for production

### Bot Strategy
- **Phase 1 (0-25%)**: Strategic waiting and observation, reacts to human bids
- **Phase 2 (25-75%)**: Mid-game engagement with reactive bidding
- **Phase 3 (75-100%+)**: Aggressive bidding with time extensions until max bid is reached

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11 or higher** installed
  - Check version: `python --version`
  - Download from: [python.org](https://www.python.org/downloads/)
  
- **Git** installed (for version control)
  - Check: `git --version`
  - Download from: [git-scm.com](https://git-scm.com/downloads)

- **Text Editor or IDE** (VS Code, PyCharm, etc.)

- **Web Browser** (Chrome, Firefox, Edge, etc.)

### 🚀 For Railway Deployment

**Good news!** You don't need:
- ❌ Complex configuration files
- ❌ Manual setup after deployment
- ❌ Your PC running after deployment (app runs 24/7 on Railway)

**You only need:**
- ✅ GitHub account (to host your code)
- ✅ Railway account (free tier available with $5 credit)
- ✅ That's it! Railway handles everything automatically

**Note**: No Redis, Celery, or Docker needed! This is a simplified Django-only version with `railway.json` configuration.

---

## 🚀 Quick Start

### Step 1: Download/Clone the Project

If you have the project files locally, navigate to the project directory:

```bash
cd "G:\My Drive\Prakruti"
```

Or if cloning from GitHub:

```bash
git clone https://github.com/YOUR_USERNAME/auction-bot.git
cd auction-bot
```

### Step 2: Install Python Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

**What this does**: Installs all required Python packages (Django, DRF, etc.)

**Expected output**: You'll see packages being downloaded and installed. Wait for it to complete.

**If you get errors**: 
- Make sure Python is installed correctly
- Try: `python -m pip install -r requirements.txt`
- On Windows, you might need to run as Administrator

### Step 3: Setup Database

Create the database tables:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to create tables
python manage.py migrate
```

**What this does**: Creates all database tables (users, auctions, bids, etc.)

**Expected output**: You'll see "Applying migrations..." messages and "OK" for each one.

### Step 4: Create Admin User (Optional but Recommended)

```bash
python manage.py createsuperuser
```

**What this does**: Creates an admin account to access the admin panel

**You'll be asked for**:
- Username: (choose any username)
- Email: (your email, optional)
- Password: (choose a strong password)
- Password confirmation: (enter same password)

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

**What this does**: Starts the Django development server

**Expected output**: 
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 6: Access the Application

Open your web browser and visit:

- **Home Page**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/swagger/
- **API Root**: http://localhost:8000/api/

**Congratulations!** Your auction bot is now running locally! 🎉

---

## 📁 Project Structure

```
auction_bot/
├── auction_bot/              # Main Django project
│   ├── settings.py           # Project settings
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
│
├── auctions/                  # Auctions application
│   ├── models.py             # Database models (Auction, Bid, etc.)
│   ├── views.py              # API and frontend views
│   ├── serializers.py        # API serializers
│   ├── bot_logic.py          # Core bot bidding logic
│   ├── bot_runner.py         # Threading-based bot runner
│   ├── admin.py              # Admin interface
│   └── urls.py               # App URL routing
│
├── users/                     # User management app
│   ├── models.py             # User model
│   ├── views.py              # Authentication views
│   └── serializers.py        # User serializers
│
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── auctions/             # Auction pages
│   └── users/                # User pages
│
├── static/                    # Static files (CSS, JS)
│   ├── css/
│   └── js/
│
├── requirements.txt          # Python dependencies
├── railway.json              # Railway deployment config
├── manage.py                 # Django management script
└── README.md                 # This file
```

---

## 🎮 How to Use

### 1. Register a New User

1. Go to: http://localhost:8000/api/auth/login/
2. Click "Register here" link
3. Fill in the form:
   - Username: Choose a unique username
   - Email: Your email address
   - Password: At least 8 characters
   - Confirm Password: Same as password
4. Click "Register"
5. You'll be automatically logged in

### 2. Create an Auction

1. After logging in, click "Create Auction" in the navigation
2. Fill in the form:
   - **Title**: Name of your auction (e.g., "Vintage Watch")
   - **Description**: Details about the item
   - **Start Price**: Starting bid amount (e.g., 1000)
   - **Max Bid**: Bot's maximum bid limit (e.g., 10000)
   - **Duration**: Auction duration in seconds (e.g., 90)
   - **Bot Active**: Check to enable bot bidding
3. Click "Create Auction"
4. You'll be redirected to your auction

### 3. Start an Auction

1. Go to "My Auctions" from the navigation
2. Find your auction in the list
3. Click the "Start" button next to your auction
4. The auction will begin and the bot will start bidding!

### 4. Place Bids

1. Go to the home page or click on an active auction
2. On the auction detail page, you'll see the bidding form
3. Enter your bid amount (must be higher than current price)
4. Select increment (₹100, ₹500, or ₹1000)
5. Click "Place Bid"
6. Your bid will be recorded and the bot may react!

### 5. View Statistics

1. Click "Statistics" in the navigation
2. View overall auction statistics
3. See total auctions, active auctions, completed auctions, etc.

---

## 🚀 Deployment

### Deploy to Railway (Recommended)

**Step 1**: Upload to GitHub
- Push your code to GitHub
- Make sure `railway.json` is included in the repository

**Step 2**: Deploy on Railway
- Sign up at [railway.app](https://railway.app)
- Create a new project from your GitHub repository
- Railway will automatically detect `railway.json` and configure everything
- Add a PostgreSQL database from Railway's services
- Set environment variables:
  - `SECRET_KEY` - Django secret key
  - `DEBUG` - Set to `False`
  - `ALLOWED_HOSTS` - Your Railway domain
  - `DATABASE_URL` - Automatically provided by Railway's PostgreSQL
- Deploy!

**Quick Summary**:
1. Push code to GitHub
2. Sign up on Railway.app
3. Create new project from GitHub repository
4. Add PostgreSQL database
5. Railway uses `railway.json` for automatic deployment
6. Your app is live!

---

## 🎯 Bot Strategy Explained

The bot operates in three distinct phases:

### Phase 1: Strategic Start (0-25% of time)

**Behavior**:
- Waits through 75% of Phase 1 (observes)
- If human bids → waits 1-3 seconds, then reacts with a bid
- If no human bids → places one bid in the last 25% of Phase 1

**Purpose**: Simulates human-like observation and slow engagement

### Phase 2: Mid-Game (25-75% of time)

**Behavior**:
- Waits through 75% of Phase 2
- If human bids → waits 1-3 seconds, then reacts
- If no human bids → places one bid near the end

**Purpose**: Ensures steady price escalation

### Phase 3: Competitive End (75-100%+)

**Behavior**:
- Every second, 30% chance to bid
- Each bid extends auction time by 5 seconds
- Continues until max bid is reached or auction ends

**Purpose**: Creates competitive end-game bidding

**Key Rules**:
- Bot never exceeds its max_bid limit
- Only human bidders can win
- Bot's role is to raise prices strategically

---

## 📚 Documentation

### Detailed Guides

- **`GITHUB_SETUP.md`** - Complete guide to upload your code to GitHub
  - Step-by-step instructions
  - Screenshot descriptions
  - Troubleshooting tips

- **`railway.json`** - Railway deployment configuration
  - Build and start commands
  - Health check settings
  - Automatic deployment configuration

- **`HOW_TO_RUN.md`** - Local development guide
  - Setting up locally
  - Running the server
  - Testing the application
  - Common issues and solutions

- **`API_DOCUMENTATION.md`** - Complete API reference
  - All endpoints documented
  - Request/response examples
  - Authentication guide
  - Error handling

---

## 🔧 Tech Stack

- **Backend Framework**: Django 4.2.7
- **API Framework**: Django REST Framework 3.14.0
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, JavaScript
- **Server**: Gunicorn (production)
- **Static Files**: WhiteNoise
- **Deployment**: Railway.app

---

## 🐛 Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError`
- **Solution**: Run `pip install -r requirements.txt`

**Problem**: `No such table` error
- **Solution**: Run `python manage.py migrate`

**Problem**: Port 8000 already in use
- **Solution**: Use different port: `python manage.py runserver 8001`

**Problem**: Can't access admin panel
- **Solution**: Create superuser: `python manage.py createsuperuser`

For more troubleshooting, see `HOW_TO_RUN.md`

---

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## 🙏 Acknowledgments

- Django and Django REST Framework
- Bootstrap for the beautiful UI
- Railway for hosting platform

---

## 📞 Support

If you encounter any issues:

1. Check the documentation files
2. Review error messages in the terminal
3. Check Django logs in `logs/auction.log`
4. Review the troubleshooting sections in the guides

---

**Built with ❤️ using Django**

**Ready to deploy?** Push to GitHub and deploy on Railway! 🚀

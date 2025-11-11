# 🚀 Complete Guide: How to Run the Auction Bot Locally

This comprehensive guide will help you set up and run the Auction Bot on your local computer step-by-step.

## 📋 Important: Why Run Locally?

### 🎯 Purpose of Local Development

**You DON'T need to run locally for Render deployment**, but local testing helps you:

1. **Test Before Deploying**: Make sure everything works before going live
2. **Develop Features**: Add new features and test them locally first
3. **Debug Issues**: Easier to debug locally than on production
4. **Learn the System**: Understand how the bot works before deploying
5. **Practice**: Get familiar with the application

### 🚀 For Production Deployment

**For Render deployment, you only need**:
- ✅ Code on GitHub
- ✅ Render account
- ✅ That's it! Render handles everything

**You DON'T need**:
- ❌ Local server running
- ❌ Local database
- ❌ Your PC to stay on

**Once deployed on Render, your app runs 24/7 on Render's servers!**

---

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Step 1: Install Dependencies](#step-1-install-dependencies)
3. [Step 2: Setup Database](#step-2-setup-database)
4. [Step 3: Create Admin User](#step-3-create-admin-user)
5. [Step 4: Run the Server](#step-4-run-the-server)
6. [Step 5: Access the Application](#step-5-access-the-application)
7. [Testing the Application](#testing-the-application)
8. [Troubleshooting](#-troubleshooting)

---

## 📋 Prerequisites

Before you start, make sure you have:

### 1. Python 3.11 or Higher

**Check if Python is installed**:
```bash
python --version
```

**Expected output**: `Python 3.11.x` or higher (like `Python 3.13.7`)

**If Python is not installed**:
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.11+ version
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation
5. Restart your terminal/command prompt
6. Verify: `python --version`

### 2. pip (Python Package Manager)

**Check if pip is installed**:
```bash
pip --version
```

**Expected output**: `pip 23.x.x` or similar

**If pip is not installed**:
- Usually comes with Python
- If missing: `python -m ensurepip --upgrade`

### 3. Terminal/Command Prompt Access

**Windows**:
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter

**Mac/Linux**:
- Open Terminal application
- Or press `Ctrl + Alt + T`

### 4. Text Editor (Optional but Recommended)

- **VS Code**: [code.visualstudio.com](https://code.visualstudio.com/)
- **PyCharm**: [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
- **Sublime Text**: [sublimetext.com](https://www.sublimetext.com/)

---

## Step 1: Install Dependencies

**What this does**: Installs all required Python packages (Django, DRF, etc.)

### Detailed Steps:

1. **Open Terminal/Command Prompt**

2. **Navigate to Project Directory**:
   ```bash
   cd "G:\My Drive\Prakruti"
   ```
   **Replace with your actual project path**

3. **Verify You're in the Right Place**:
   ```bash
   dir
   ```
   (Windows) or
   ```bash
   ls
   ```
   (Mac/Linux)
   
   **You should see**: `manage.py`, `requirements.txt`, `auction_bot/`, etc.

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **What Happens**:
   - pip reads `requirements.txt`
   - Downloads and installs each package
   - This takes 2-5 minutes depending on your internet

6. **Expected Output**:
   ```
   Collecting Django==4.2.7
   Downloading Django-4.2.7-py3-none-any.whl (8.0 MB)
   ...
   Successfully installed Django-4.2.7 djangorestframework-3.14.0 ...
   ```

7. **Verify Installation**:
   ```bash
   python -c "import django; print(django.get_version())"
   ```
   **Should output**: `4.2.7`

### Common Issues:

**Issue**: `'pip' is not recognized`
- **Solution**: Use `python -m pip install -r requirements.txt`

**Issue**: `Permission denied`
- **Solution Windows**: Run Command Prompt as Administrator
- **Solution Mac/Linux**: Use virtual environment (recommended)

**Issue**: `Module not found` after installation
- **Solution**: Make sure you're using the same Python that has the packages installed

---

## Step 2: Setup Database

**What this does**: Creates all database tables needed for the application.

### Detailed Steps:

1. **Create Migration Files**:
   ```bash
   python manage.py makemigrations
   ```
   
   **What this does**: 
   - Analyzes your models (Auction, Bid, User, etc.)
   - Creates migration files that describe database changes
   - These files are in `auctions/migrations/` and `users/migrations/`

   **Expected Output**:
   ```
   Migrations for 'users':
     users\migrations\0001_initial.py
       - Create model User
   Migrations for 'auctions':
     auctions\migrations\0001_initial.py
       - Create model Auction
       - Create model Bid
       - Create model AuctionLog
   ```

   **If you see "No changes detected"**:
   - This is fine if migrations already exist
   - Continue to next step

2. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```
   
   **What this does**:
   - Reads migration files
   - Creates actual database tables in SQLite
   - Links tables together with foreign keys

   **Expected Output**:
   ```
   Operations to perform:
     Apply all migrations: admin, auth, authtoken, contenttypes, sessions, users, auctions
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     ...
     Applying auctions.0001_initial... OK
   ```

   **What happened**: 
   - Database file `db.sqlite3` was created (if it didn't exist)
   - All tables are now ready

3. **Verify Database**:
   - Check that `db.sqlite3` file exists in your project folder
   - This is your SQLite database file

### Common Issues:

**Issue**: `No such file or directory: 'db.sqlite3'`
- **Solution**: This is normal - the file is created during migration
- Run `python manage.py migrate` again

**Issue**: `Table already exists`
- **Solution**: Database is already set up, you can continue
- Or delete `db.sqlite3` and run migrations again (⚠️ deletes all data)

---

## Step 3: Create Admin User

**What this does**: Creates a superuser account to access the Django admin panel.

### Detailed Steps:

1. **Run Command**:
   ```bash
   python manage.py createsuperuser
   ```

2. **Enter Username**:
   ```
   Username: admin
   ```
   - Choose any username you like
   - Press Enter

3. **Enter Email** (Optional):
   ```
   Email address: your.email@example.com
   ```
   - Enter your email or leave blank
   - Press Enter

4. **Enter Password**:
   ```
   Password: 
   ```
   - Type your password (it won't show on screen - this is normal!)
   - Choose a strong password
   - Press Enter

5. **Confirm Password**:
   ```
   Password (again): 
   ```
   - Type the same password again
   - Press Enter

6. **Success Message**:
   ```
   Superuser created successfully.
   ```

7. **What You Created**:
   - A user account with admin privileges
   - Can access `/admin/` panel
   - Can manage all data in the database

### Common Issues:

**Issue**: `Password too common`
- **Solution**: Choose a more complex password (mix of letters, numbers, symbols)

**Issue**: `This field is required`
- **Solution**: Make sure you entered a value for username

**Issue**: `A user with that username already exists`
- **Solution**: Choose a different username

---

## Step 4: Run the Server

**What this does**: Starts the Django development server so you can access the application.

### Detailed Steps:

1. **Make Sure You're in Project Directory**:
   ```bash
   cd "G:\My Drive\Prakruti"
   ```

2. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

3. **Expected Output**:
   ```
   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   Django version 4.2.7, using settings 'auction_bot.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

4. **What This Means**:
   - ✅ Server is running
   - ✅ No errors detected
   - ✅ Available at http://127.0.0.1:8000/
   - ⚠️ **Keep this terminal window open!** Closing it stops the server

5. **Server is Running**:
   - The server will automatically reload when you change code
   - You'll see messages when files change
   - To stop: Press `Ctrl + C` (or `Ctrl + Break` on Windows)

### Running on Different Port:

If port 8000 is busy:
```bash
python manage.py runserver 8001
```
Then access at: http://localhost:8001/

### Common Issues:

**Issue**: `That port is already in use`
- **Solution**: 
  - Use different port: `python manage.py runserver 8001`
  - Or find and close the program using port 8000

**Issue**: `Address already in use`
- **Solution**: Same as above - use different port

**Issue**: Server starts but shows errors
- **Solution**: Check the error messages
- Common: Missing migrations, database issues
- Run `python manage.py migrate` if needed

---

## Step 5: Access the Application

**What this does**: Opens the application in your web browser.

### Detailed Steps:

1. **Open Web Browser**:
   - Chrome, Firefox, Edge, Safari - any browser works

2. **Visit Home Page**:
   - Go to: http://localhost:8000/
   - Or: http://127.0.0.1:8000/
   - You should see the Auction Bot home page!

3. **Available Pages**:

   **Home Page**:
   - URL: http://localhost:8000/
   - Shows: Active auctions, recent completed auctions
   - **What to expect**: List of auctions or "No active auctions" message

   **Admin Panel**:
   - URL: http://localhost:8000/admin/
   - Shows: Django admin interface
   - **Login with**: The superuser you created in Step 3
   - **What you can do**: Manage users, auctions, bids

   **API Documentation**:
   - URL: http://localhost:8000/swagger/
   - Shows: Interactive API documentation
   - **What you can do**: Test API endpoints, see all available endpoints

   **API Root**:
   - URL: http://localhost:8000/api/
   - Shows: API root with available endpoints

4. **Verify Everything Works**:
   - ✅ Home page loads
   - ✅ Can navigate between pages
   - ✅ Admin panel accessible
   - ✅ No error pages

---

## 🧪 Testing the Application

### Test 1: Register a New User

1. **Go to Login Page**:
   - Click "Login" in navigation or go to: http://localhost:8000/api/auth/login/

2. **Click "Register here"**:
   - Or go directly to: http://localhost:8000/api/auth/register/

3. **Fill Registration Form**:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Confirm Password: `testpass123`
   - Phone: (optional)

4. **Click "Register"**:
   - You should be automatically logged in
   - Redirected to home page
   - See your username in navigation

### Test 2: Create an Auction

1. **Click "Create Auction"** in navigation

2. **Fill the Form**:
   - Title: `Test Auction`
   - Description: `This is a test auction`
   - Start Price: `1000`
   - Max Bid: `10000`
   - Duration: `90`
   - Bot Active: ✅ (checked)

3. **Click "Create Auction"**:
   - You'll be redirected to auction detail page
   - Auction status: "Pending"

### Test 3: Start an Auction

1. **Go to "My Auctions"**:
   - Click in navigation

2. **Find Your Auction**:
   - Should see "Test Auction" in the list
   - Status: "Pending"

3. **Click "Start" Button**:
   - Auction status changes to "Active"
   - Bot starts bidding automatically!
   - Timer starts counting down

### Test 4: Place a Bid

1. **Go to Active Auction**:
   - Click on auction from home page or "My Auctions"

2. **Enter Bid Amount**:
   - Current price shows (e.g., ₹1000)
   - Enter higher amount: `1500`
   - Select increment: `500`

3. **Click "Place Bid"**:
   - Bid is recorded
   - Current price updates
   - Bot may react with its own bid!

### Test 5: View Statistics

1. **Click "Statistics"** in navigation

2. **View Dashboard**:
   - Total auctions count
   - Active auctions count
   - Completed auctions count
   - Total bids count

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'django'"

**Error Message**:
```
ModuleNotFoundError: No module named 'django'
```

**Cause**: Django is not installed

**Solution**:
```bash
pip install -r requirements.txt
```

**Verify**:
```bash
python -c "import django; print(django.get_version())"
```

---

### Problem: "No such file or directory: 'db.sqlite3'"

**Error Message**:
```
django.db.utils.OperationalError: no such table
```

**Cause**: Database migrations not run

**Solution**:
```bash
python manage.py migrate
```

**This creates**: The `db.sqlite3` file and all tables

---

### Problem: "That port is already in use"

**Error Message**:
```
Error: That port is already in use.
```

**Cause**: Another program is using port 8000

**Solution Option 1**: Use different port
```bash
python manage.py runserver 8001
```
Then access at: http://localhost:8001/

**Solution Option 2**: Find and close the program
```bash
# Windows - find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

---

### Problem: "Table 'X' already exists"

**Error Message**:
```
django.db.utils.OperationalError: table "X" already exists
```

**Cause**: Database already has tables, but migrations think they don't exist

**Solution Option 1**: Continue (if data exists, don't do this)
```bash
# Mark migrations as applied without running them
python manage.py migrate --fake
```

**Solution Option 2**: Fresh start (⚠️ deletes all data)
```bash
# Delete database
# Windows:
del db.sqlite3

# Mac/Linux:
rm db.sqlite3

# Recreate
python manage.py migrate
```

---

### Problem: "SECRET_KEY not set"

**Error Message**:
```
ImproperlyConfigured: The SECRET_KEY setting must not be empty
```

**Cause**: SECRET_KEY not configured

**Solution**: Default in settings.py will work for development. For production, set in environment variables.

---

### Problem: Static files not loading (404 errors)

**Error**: CSS/JS files return 404

**Cause**: Static files not collected

**Solution**:
```bash
python manage.py collectstatic --noinput
```

**Note**: For development, Django serves static files automatically. This is mainly for production.

---

### Problem: "Can't access admin panel"

**Error**: 404 or login doesn't work

**Cause**: Superuser not created or wrong credentials

**Solution**:
```bash
# Create superuser
python manage.py createsuperuser

# Follow prompts
# Then login at http://localhost:8000/admin/
```

---

### Problem: Bot not bidding

**Symptoms**: Auction is active but bot doesn't bid

**Possible Causes**:
1. Bot is disabled for that auction
2. Bot reached max_bid limit
3. Auction ended

**Check**:
1. Go to auction detail page
2. Check "Bot Active" status
3. Check "Bot Current Bid" vs "Max Bid"
4. Check remaining time

**Solution**: 
- Make sure "Bot Active" is checked when creating auction
- Ensure max_bid is high enough
- Bot starts automatically when auction starts

---

### Problem: "Permission denied" when installing

**Error**: Permission errors during `pip install`

**Solution Windows**:
- Run Command Prompt as Administrator
- Right-click Command Prompt → "Run as administrator"

**Solution Mac/Linux**:
- Use virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # Mac/Linux
  venv\Scripts\activate     # Windows
  pip install -r requirements.txt
  ```

---

## ✅ Quick Reference Commands

### Setup (First Time)
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Daily Use
```bash
# Start server
python manage.py runserver

# Stop server
# Press Ctrl + C in the terminal
```

### If Something Breaks
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Reset database (⚠️ deletes all data)
del db.sqlite3  # Windows
rm db.sqlite3   # Mac/Linux
python manage.py migrate

# Check for errors
python manage.py check
```

---

## 🎯 What Should Work

After completing all steps:

- ✅ Server runs without errors
- ✅ Can access home page
- ✅ Can register/login users
- ✅ Can create auctions
- ✅ Can start auctions
- ✅ Bot bids automatically
- ✅ Can place bids
- ✅ Admin panel accessible
- ✅ API documentation accessible

---

## 📝 Next Steps

Once everything is working locally:

1. **Test all features**:
   - Create multiple auctions
   - Test bidding
   - Check bot behavior
   - View statistics

2. **Make improvements**:
   - Customize the UI
   - Add features
   - Fix any bugs

3. **Deploy to production**:
   - Follow `GITHUB_SETUP.md` to upload to GitHub
   - Follow `RENDER_DEPLOYMENT.md` to deploy on Render
   - **Once deployed, you don't need to run locally anymore!**

---

## 📞 Still Having Issues?

1. **Check Error Messages**: Read them carefully - they usually tell you what's wrong
2. **Check Logs**: Look in `logs/auction.log` for detailed error messages
3. **Verify Prerequisites**: Make sure Python 3.11+ is installed
4. **Try Fresh Start**: Delete `db.sqlite3` and run migrations again
5. **Check Documentation**: Review `README.md` and `API_DOCUMENTATION.md`

---

**Your Auction Bot is now running locally! 🎉**

**Ready to deploy? Follow `GITHUB_SETUP.md` then `RENDER_DEPLOYMENT.md`! 🚀**

**Remember**: Once deployed on Render, your app runs 24/7 on Render's servers - you don't need your PC running!

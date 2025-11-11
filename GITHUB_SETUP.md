# 📤 Complete GitHub Setup Guide

This guide will walk you through uploading your Auction Bot project to GitHub step-by-step.

## 📋 Prerequisites

Before starting, make sure you have:

1. ✅ **Git installed** on your computer
   - Check: Open terminal and type `git --version`
   - If not installed: Download from [git-scm.com](https://git-scm.com/downloads)
   - Install with default settings

2. ✅ **GitHub account** created
   - Go to [github.com](https://github.com)
   - Click "Sign up" if you don't have an account
   - Verify your email address

3. ✅ **Project files ready**
   - Make sure all your project files are in one folder
   - You should see files like `manage.py`, `requirements.txt`, etc.

---

## 🎯 Step-by-Step Instructions

### Step 1: Open Terminal/Command Prompt

**On Windows**:
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter
- Navigate to your project folder:
  ```bash
  cd "G:\My Drive\Prakruti"
  ```

**On Mac/Linux**:
- Open Terminal
- Navigate to your project folder:
  ```bash
  cd /path/to/your/project
  ```

**Verify you're in the right folder**:
- Type `dir` (Windows) or `ls` (Mac/Linux)
- You should see `manage.py`, `requirements.txt`, etc.

---

### Step 2: Initialize Git Repository

**What this does**: Creates a new Git repository in your project folder to track changes.

**Command**:
```bash
git init
```

**Expected output**:
```
Initialized empty Git repository in G:\My Drive\Prakruti\.git\
```

**What happened**: Git created a hidden `.git` folder to track your files.

---

### Step 3: Add All Files to Git

**What this does**: Tells Git to track all your project files.

**Command**:
```bash
git add .
```

**Expected output**: (No output is normal - it means success!)

**What happened**: All files are now staged (ready to be committed).

**Note**: Files in `.gitignore` (like `db.sqlite3`, `venv/`, etc.) won't be added - this is correct!

---

### Step 4: Create Your First Commit

**What this does**: Saves a snapshot of all your files with a message.

**Command**:
```bash
git commit -m "Initial commit: Smart Auction Bot - Django version"
```

**Expected output**:
```
[main (or master) (root-commit) abc1234] Initial commit: Smart Auction Bot - Django version
 X files changed, Y insertions(+)
```

**What happened**: Git saved all your files as the first version.

**If you see an error about email/name**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
Then run the commit command again.

---

### Step 5: Create GitHub Repository

**What this does**: Creates an empty repository on GitHub where you'll upload your code.

**Detailed Steps**:

1. **Go to GitHub**:
   - Open your web browser
   - Go to [github.com](https://github.com)
   - Sign in to your account

2. **Click "New Repository"**:
   - Look for a green "New" button (or a "+" icon in the top right)
   - Click it, then select "New repository"

3. **Fill in Repository Details**:
   - **Repository name**: `auction-bot` (or any name you like)
     - Use lowercase letters, numbers, and hyphens
     - No spaces allowed
   - **Description**: `Smart Automated Bidding System with Phase-Based Bot Strategy`
   - **Visibility**: 
     - Choose **Public** (anyone can see) or **Private** (only you)
     - For this project, Public is fine
   - **IMPORTANT**: 
     - ❌ **DO NOT** check "Add a README file"
     - ❌ **DO NOT** check "Add .gitignore"
     - ❌ **DO NOT** check "Choose a license"
   - Leave everything else as default

4. **Click "Create repository"**:
   - A new page will open with setup instructions
   - **Don't follow those instructions yet!** We'll use our own commands.

5. **Copy Your Repository URL**:
   - On the new page, you'll see a URL like:
     ```
     https://github.com/YOUR_USERNAME/auction-bot.git
     ```
   - **Copy this URL** - you'll need it in the next step
   - Replace `YOUR_USERNAME` with your actual GitHub username

---

### Step 6: Connect Local Repository to GitHub

**What this does**: Links your local Git repository to the GitHub repository.

**Command** (replace with your actual URL):
```bash
git remote add origin https://github.com/YOUR_USERNAME/auction-bot.git
```

**Example** (if your username is `john` and repo is `auction-bot`):
```bash
git remote add origin https://github.com/john/auction-bot.git
```

**Expected output**: (No output means success!)

**What happened**: Git now knows where to push your code.

**If you get an error "remote origin already exists"**:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/auction-bot.git
```

---

### Step 7: Rename Branch to Main

**What this does**: Ensures your branch is named "main" (GitHub's standard).

**Command**:
```bash
git branch -M main
```

**Expected output**: (No output means success!)

**What happened**: Your branch is now called "main" instead of "master".

---

### Step 8: Push Code to GitHub

**What this does**: Uploads all your code to GitHub.

**Command**:
```bash
git push -u origin main
```

**What will happen**:
1. GitHub will ask you to sign in
2. You might need to authenticate
3. Your files will start uploading

**Authentication Options**:

**Option A: GitHub Desktop** (Easiest)
- Download [GitHub Desktop](https://desktop.github.com/)
- Sign in with your GitHub account
- It will handle authentication automatically

**Option B: Personal Access Token** (Recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Auction Bot"
4. Select scopes: Check "repo"
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. When Git asks for password, paste the token instead

**Option C: SSH Key** (Advanced)
- Follow GitHub's SSH setup guide
- More secure but requires more setup

**Expected output** (after authentication):
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to X threads
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To https://github.com/YOUR_USERNAME/auction-bot.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**What happened**: All your code is now on GitHub! 🎉

---

### Step 9: Verify Upload

**What this does**: Confirms your code is on GitHub.

**Steps**:

1. **Go to your GitHub repository**:
   - Open: `https://github.com/YOUR_USERNAME/auction-bot`
   - Replace `YOUR_USERNAME` with your actual username

2. **Check the files**:
   - You should see all your project files
   - Look for: `manage.py`, `requirements.txt`, `render.yaml`, etc.
   - You should see folders: `auction_bot/`, `auctions/`, `users/`, `templates/`, etc.

3. **Check for important files**:
   - ✅ `render.yaml` should be there (for Render deployment)
   - ✅ `requirements.txt` should be there
   - ✅ `README.md` should be there
   - ✅ `.gitignore` should be there

**If files are missing**:
- Make sure you ran `git add .` in Step 3
- Check that files aren't in `.gitignore`
- Try pushing again: `git push origin main`

---

## 🔄 Making Changes and Updating GitHub

After you make changes to your code locally:

### Step 1: Check What Changed

```bash
git status
```

**Shows**: Which files were modified, added, or deleted

### Step 2: Add Changed Files

```bash
git add .
```

**Or add specific files**:
```bash
git add filename.py
```

### Step 3: Commit Changes

```bash
git commit -m "Description of what you changed"
```

**Examples**:
```bash
git commit -m "Fixed bot bidding logic"
git commit -m "Updated UI design"
git commit -m "Added new features"
```

### Step 4: Push to GitHub

```bash
git push origin main
```

**What happens**: Your changes are uploaded to GitHub and Render will automatically redeploy!

---

## ✅ What Should Be on GitHub

Your repository should contain:

### Essential Files:
- ✅ `manage.py` - Django management script
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render deployment configuration
- ✅ `README.md` - Project documentation
- ✅ `.gitignore` - Files to exclude from Git

### Project Folders:
- ✅ `auction_bot/` - Main Django project
- ✅ `auctions/` - Auctions app
- ✅ `users/` - User management app
- ✅ `templates/` - HTML templates
- ✅ `static/` - CSS and JavaScript files

### Documentation:
- ✅ `GITHUB_SETUP.md` - This file
- ✅ `RENDER_DEPLOYMENT.md` - Deployment guide
- ✅ `HOW_TO_RUN.md` - Local setup guide
- ✅ `API_DOCUMENTATION.md` - API reference

### Should NOT Be on GitHub:
- ❌ `db.sqlite3` - Local database (in .gitignore)
- ❌ `venv/` - Virtual environment (in .gitignore)
- ❌ `__pycache__/` - Python cache (in .gitignore)
- ❌ `.env` - Environment variables (in .gitignore)
- ❌ `logs/` - Log files (in .gitignore)
- ❌ `staticfiles/` - Collected static files (in .gitignore)

---

## 🐛 Troubleshooting

### Problem: "fatal: not a git repository"

**Error**: `fatal: not a git repository (or any of the parent directories): .git`

**Solution**:
```bash
# Make sure you're in the project directory
cd "G:\My Drive\Prakruti"

# Initialize Git
git init
```

---

### Problem: "remote origin already exists"

**Error**: `fatal: remote origin already exists`

**Solution**:
```bash
# Remove existing remote
git remote remove origin

# Add it again with correct URL
git remote add origin https://github.com/YOUR_USERNAME/auction-bot.git
```

---

### Problem: "Authentication failed"

**Error**: `remote: Support for password authentication was removed`

**Solution**: Use a Personal Access Token instead of password:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select "repo" scope
4. Copy token
5. Use token as password when pushing

---

### Problem: "Permission denied"

**Error**: `Permission denied (publickey)`

**Solution**: You're trying to use SSH but don't have keys set up. Use HTTPS instead:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/auction-bot.git
```

---

### Problem: Files not showing on GitHub

**Possible causes**:
1. Files are in `.gitignore` - Check `.gitignore` file
2. Files weren't added - Run `git add .` again
3. Files weren't committed - Run `git commit -m "message"`
4. Files weren't pushed - Run `git push origin main`

**Check what's tracked**:
```bash
git ls-files
```

---

### Problem: "Updates were rejected"

**Error**: `Updates were rejected because the remote contains work that you do not have locally`

**Solution**: Pull first, then push:
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

---

## 🎉 Success Checklist

After completing all steps, you should have:

- ✅ Git repository initialized locally
- ✅ All files committed
- ✅ GitHub repository created
- ✅ Local repository connected to GitHub
- ✅ All code pushed to GitHub
- ✅ Can see all files on GitHub website
- ✅ `render.yaml` is visible on GitHub

---

## 🚀 Next Steps

Now that your code is on GitHub:

1. **Verify everything is there** - Check the GitHub website
2. **Deploy on Render** - Follow `RENDER_DEPLOYMENT.md`
3. **Share your repository** - Others can now see your code!

---

## 📞 Need Help?

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Help**: https://docs.github.com
- **GitHub Support**: https://support.github.com

---

**Your code is now on GitHub! Ready to deploy? Follow `RENDER_DEPLOYMENT.md` next! 🚀**

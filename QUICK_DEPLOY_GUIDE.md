# 🚀 Quick Deployment Guide

## ✅ Your app is now production-ready!

I've made the necessary changes to prepare your Flask application for deployment.

---

## 📦 What Was Changed

1. ✅ Added production WSGI server (Gunicorn)
2. ✅ Added environment variable configuration
3. ✅ Removed hardcoded debug mode
4. ✅ Added Flask secret key configuration
5. ✅ Created production entry point (`wsgi.py`)
6. ✅ Created `Procfile` for platform deployment
7. ✅ Added `.gitignore` for security
8. ✅ Created deployment configuration files

---

## 🎯 Recommended: Deploy to Render (Easiest)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your repository

### Step 3: Configure Service
- **Name**: `chain-explorer` (or any name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT wsgi:app --timeout 120 --workers 2`

### Step 4: Set Environment Variables
In Render dashboard, add these environment variables:
- `FLASK_ENV` = `production`
- `FLASK_DEBUG` = `False`
- `SECRET_KEY` = (generate a random string, e.g., use `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATA_FILE` = `combined_block.csv`

### Step 5: Deploy
1. Make sure `combined_block.csv` is committed to your repository
2. Click "Create Web Service"
3. Wait for deployment (usually 2-5 minutes)

### Step 6: Access Your App
- Render will provide a URL like: `https://chain-explorer.onrender.com`
- Your app will be live!

---

## 🚂 Alternative: Deploy to Railway

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

### Step 3: Configure
- Railway auto-detects Python
- It will use the `Procfile` automatically
- Add environment variables in the Variables tab:
  - `FLASK_ENV=production`
  - `FLASK_DEBUG=False`
  - `SECRET_KEY=<your-secret-key>`

### Step 4: Deploy
- Railway automatically deploys on git push
- Your app will be live at a Railway-provided URL

---

## 🔧 Local Testing (Before Deployment)

Test your production setup locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env file)
echo "FLASK_ENV=production" > .env
echo "FLASK_DEBUG=False" >> .env
echo "SECRET_KEY=test-secret-key" >> .env

# Test with Gunicorn (production server)
gunicorn --bind 0.0.0.0:5000 wsgi:app

# Or test with development server
python run.py
```

---

## ⚠️ Important Notes

1. **CSV File**: Make sure `combined_block.csv` is committed to your repository (or upload it separately)

2. **Secret Key**: Generate a strong secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Free Tier Limits**:
   - Render: Apps sleep after 15 minutes of inactivity (free tier)
   - Railway: Limited hours per month (free tier)
   - Consider upgrading for production use

4. **Environment Variables**: Never commit `.env` file with real secrets to Git

---

## 🆘 Troubleshooting

### App won't start
- Check that `combined_block.csv` exists in the project root
- Verify all environment variables are set
- Check build logs in your platform's dashboard

### Slow performance
- Increase Gunicorn workers: `--workers 4`
- Consider upgrading from free tier

### Data not loading
- Verify CSV file is in the repository
- Check file path matches `DATA_FILE` environment variable

---

## 📝 Next Steps After Deployment

1. ✅ Test all routes work correctly
2. ✅ Verify API endpoints respond
3. ✅ Check analytics pages load
4. ✅ Test query functionality
5. ✅ Monitor logs for errors
6. ✅ Set up custom domain (optional)

---

## ❌ About Netlify

**Can you deploy on Netlify?** 

**Short answer: Not recommended.**

Netlify is designed for:
- Static websites
- Serverless functions (with time limits)

Your Flask app is:
- A full web application
- Requires persistent server
- Loads data at startup

**Better alternatives**: Render, Railway, Heroku, Fly.io

If you absolutely must use Netlify, you'd need to:
- Refactor to serverless functions
- Handle cold starts
- Work around 10-second execution limits
- Significant code changes required

**Recommendation**: Use Render or Railway instead - they're designed for Flask apps!

---

## 🎉 You're Ready!

Your Flask application is now configured for production deployment. Choose a platform above and follow the steps!


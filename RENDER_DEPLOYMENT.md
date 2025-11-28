# 🚀 Render Deployment Guide - Chain Explorer

## ✅ Your app is now 100% Render-ready!

All necessary files have been created and configured for seamless Render deployment.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [x] ✅ `wsgi.py` - Production entry point
- [x] ✅ `Procfile` - Render start command
- [x] ✅ `render.yaml` - Auto-configuration file
- [x] ✅ `requirements.txt` - All dependencies including Gunicorn
- [x] ✅ `runtime.txt` - Python version specification
- [x] ✅ `.gitignore` - Security best practices
- [x] ✅ Production-ready `app.py` with environment variables
- [ ] ⚠️ `combined_block.csv` - Must be in your repository

---

## 🎯 Step-by-Step Render Deployment

### Step 1: Prepare Your Repository

1. **Commit all files to Git:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify `combined_block.csv` is included:**
   - This file MUST be in your repository
   - Render needs it to run your app
   - If it's large (>100MB), consider using Git LFS

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended for easy deployment)

### Step 3: Create New Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Select your repository: **"Chain Explorer"** (or your repo name)
4. Click **"Connect"**

### Step 4: Configure Service (Auto or Manual)

#### Option A: Auto-Configure (Recommended - Uses render.yaml)

If you have `render.yaml` in your repo (which you do!):
- Render will auto-detect and use it
- Most settings will be pre-filled
- Just verify and click **"Create Web Service"**

#### Option B: Manual Configuration

If you prefer manual setup:

**Basic Settings:**
- **Name**: `chain-explorer` (or any name you prefer)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (root of repo)

**Build & Deploy:**
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT wsgi:app --timeout 120 --workers 2 --threads 4`

**Plan:**
- Start with **Free** plan (can upgrade later)

### Step 5: Set Environment Variables

In the Render dashboard, go to **"Environment"** tab and add:

| Key | Value | Notes |
|-----|-------|-------|
| `FLASK_ENV` | `production` | Required |
| `FLASK_DEBUG` | `False` | Required for production |
| `SECRET_KEY` | `[Generate random string]` | **IMPORTANT: Generate a secure key** |
| `DATA_FILE` | `combined_block.csv` | Your data file name |
| `PORT` | *(Auto-set by Render)* | Don't set manually |

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Or use an online generator: https://randomkeygen.com/

### Step 6: Deploy!

1. Click **"Create Web Service"** or **"Save Changes"**
2. Render will start building your app
3. Watch the build logs in real-time
4. First deployment takes 3-5 minutes

### Step 7: Verify Deployment

1. Once build completes, your app will be live!
2. Render provides a URL like: `https://chain-explorer.onrender.com`
3. Test all pages:
   - Main dashboard: `https://your-app.onrender.com/`
   - Analytics: `https://your-app.onrender.com/analytics`
   - Transactions: `https://your-app.onrender.com/transactions`
   - Query: `https://your-app.onrender.com/query`

---

## 🔧 Render-Specific Optimizations

### Free Tier Considerations

**Render Free Tier:**
- Apps sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month free
- Perfect for development/testing

**To prevent sleeping:**
- Upgrade to paid plan ($7/month)
- Or use a service like UptimeRobot to ping your app every 10 minutes

### Performance Tips

1. **Gunicorn Workers:**
   - Current: 2 workers (good for free tier)
   - For more traffic: Increase to 4-8 workers

2. **Timeout Settings:**
   - Current: 120 seconds
   - Adjust if you have slow queries

3. **Memory Usage:**
   - Monitor in Render dashboard
   - Large CSV files may need more memory

---

## 🐛 Troubleshooting

### Build Fails

**Error: "Module not found"**
- Check `requirements.txt` has all dependencies
- Verify Python version in `runtime.txt`

**Error: "Port already in use"**
- Don't set PORT manually - Render handles this
- Remove PORT from environment variables

**Error: "File not found: combined_block.csv"**
- Ensure CSV file is committed to repository
- Check file name matches `DATA_FILE` env var
- Verify file is in root directory

### App Crashes After Deployment

**Check Logs:**
1. Go to Render dashboard
2. Click on your service
3. View "Logs" tab
4. Look for error messages

**Common Issues:**
- Missing environment variables → Add them
- CSV file not found → Verify file is in repo
- Memory limit exceeded → Upgrade plan or optimize code
- Import errors → Check requirements.txt

### Slow Performance

**Cold Starts (Free Tier):**
- First request after sleep is slow (normal)
- Subsequent requests are fast
- Consider upgrading to prevent sleeping

**Slow Queries:**
- Check if CSV file is very large
- Consider optimizing data loading
- Add caching if needed

---

## 📊 Monitoring Your App

### Render Dashboard Features

1. **Metrics Tab:**
   - CPU usage
   - Memory usage
   - Request count
   - Response times

2. **Logs Tab:**
   - Real-time application logs
   - Build logs
   - Error tracking

3. **Events Tab:**
   - Deployment history
   - Service events

### Health Checks

Render automatically monitors your app, but you can add a health check endpoint:

```python
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200
```

---

## 🔄 Continuous Deployment

Render automatically deploys when you push to your connected branch:

1. Make changes locally
2. Commit: `git commit -m "Your changes"`
3. Push: `git push origin main`
4. Render automatically rebuilds and deploys
5. Get notified when deployment completes

---

## 🔐 Security Checklist

- [x] ✅ Debug mode disabled in production
- [x] ✅ Secret key set via environment variable
- [x] ✅ `.env` file in `.gitignore`
- [x] ✅ No hardcoded credentials
- [x] ✅ Production WSGI server (Gunicorn)

---

## 📝 Post-Deployment Tasks

1. ✅ Test all routes work correctly
2. ✅ Verify API endpoints respond
3. ✅ Check analytics pages load
4. ✅ Test query functionality
5. ✅ Monitor logs for errors
6. ✅ Set up custom domain (optional)
7. ✅ Configure auto-deploy from Git (enabled by default)

---

## 🎉 You're All Set!

Your Flask app is now fully configured for Render deployment. Follow the steps above and your app will be live in minutes!

**Need Help?**
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Check your build logs for specific errors

---

## 📦 Files Created for Render

- ✅ `wsgi.py` - Production entry point
- ✅ `Procfile` - Start command
- ✅ `render.yaml` - Auto-configuration
- ✅ `runtime.txt` - Python version
- ✅ Updated `app.py` - Production-ready
- ✅ Updated `requirements.txt` - Includes Gunicorn
- ✅ `.gitignore` - Security

**Everything is ready! Just push to GitHub and deploy on Render! 🚀**


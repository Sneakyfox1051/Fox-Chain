# 🚀 Deploy to Render - Quick Start Guide

## ✅ Your code is now on GitHub!

Your Flask app has been successfully pushed to: **https://github.com/Sneakyfox1051/Fox-Chain.git**

---

## 🎯 Deploy to Render in 5 Minutes

### Step 1: Go to Render
Visit [render.com](https://render.com) and sign up/login

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if you haven't connected GitHub yet
4. Authorize Render to access your GitHub repositories

### Step 3: Select Your Repository
1. Find and select: **"Sneakyfox1051/Fox-Chain"**
2. Click **"Connect"**

### Step 4: Configure (Auto-Detected!)
Render will automatically detect your `render.yaml` file and configure:
- ✅ Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
- ✅ Start Command: `gunicorn --bind 0.0.0.0:$PORT wsgi:app --timeout 120 --workers 2 --threads 4`
- ✅ Python Environment
- ✅ Free Plan

**Just verify these settings match, then continue!**

### Step 5: Set Environment Variables
In the **"Environment"** tab, add these variables:

| Variable | Value |
|----------|-------|
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `False` |
| `SECRET_KEY` | Generate one (see below) |
| `DATA_FILE` | `combined_block.csv` |

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Or use: https://randomkeygen.com/ (use "CodeIgniter Encryption Keys")

### Step 6: Deploy!
1. Click **"Create Web Service"**
2. Watch the build logs
3. Wait 3-5 minutes for first deployment
4. Your app will be live! 🎉

---

## 🔗 Your App Will Be Available At:
`https://chain-explorer.onrender.com` (or similar URL provided by Render)

---

## ✅ What's Already Configured

- ✅ `wsgi.py` - Production entry point
- ✅ `Procfile` - Start command for Render
- ✅ `render.yaml` - Auto-configuration
- ✅ `runtime.txt` - Python 3.11.0
- ✅ `requirements.txt` - All dependencies including Gunicorn
- ✅ `app.py` - Production-ready with environment variables
- ✅ Health check endpoint at `/health`
- ✅ All templates and static files
- ✅ `combined_block.csv` - Your data file

---

## 🧪 Test Your Deployment

Once deployed, test these URLs:
- Homepage: `https://your-app.onrender.com/`
- Dashboard: `https://your-app.onrender.com/dashboard`
- Analytics: `https://your-app.onrender.com/analytics`
- Transactions: `https://your-app.onrender.com/transactions`
- Query: `https://your-app.onrender.com/query`
- Health Check: `https://your-app.onrender.com/health`
- API Stats: `https://your-app.onrender.com/api/stats`

---

## 📊 Monitor Your App

1. **Build Logs**: See real-time build progress
2. **Runtime Logs**: Monitor app performance
3. **Metrics**: CPU, Memory, Request count
4. **Events**: Deployment history

---

## 🆘 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Verify `combined_block.csv` is in repository
- Ensure all dependencies in `requirements.txt`

### App Crashes
- Check runtime logs
- Verify environment variables are set
- Ensure `SECRET_KEY` is set

### Slow First Request
- Normal on free tier (cold start after 15 min sleep)
- Subsequent requests are fast
- Upgrade to paid plan to prevent sleeping

---

## 🎉 You're All Set!

Your Flask app is now:
- ✅ On GitHub: https://github.com/Sneakyfox1051/Fox-Chain.git
- ✅ Ready for Render deployment
- ✅ Production-configured
- ✅ Fully documented

**Next Step**: Go to Render and deploy! 🚀

---

## 📚 Additional Resources

- **Full Deployment Guide**: See `RENDER_DEPLOYMENT.md`
- **Checklist**: See `RENDER_CHECKLIST.md`
- **General Info**: See `DEPLOYMENT_README.md`

---

**Need Help?** Check the Render dashboard logs or review the detailed guides in the repository.


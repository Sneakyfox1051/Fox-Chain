# Deployment Guide - Render

This guide will help you deploy the RAG Chatbot for Blockchain Data on Render.

## Prerequisites

1. GitHub account with the repository pushed
2. Render account (sign up at https://render.com)

## Step 1: Push to GitHub

If you haven't already:

```bash
git add .
git commit -m "Add RAG chatbot system with performance tracking"
git push origin main
```

## Step 2: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and configure everything
5. Click "Apply" to deploy

### Option B: Manual Setup

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: chain-explorer (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT wsgi:app --timeout 120 --workers 2 --threads 4`
   - **Plan**: Free (or choose paid for better performance)

5. Add Environment Variables:
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `False`
   - `SECRET_KEY`: (Generate a secure random string)
   - `DATA_FILE`: `combined_block.csv`
   - `OPENAI_API_KEY`: (Optional - your OpenAI API key if you want LLM features)

6. Click "Create Web Service"

## Step 3: Upload Data File

Since `combined_block.csv` is in the repository, it will be deployed automatically. If you need to update it:

1. Go to your service dashboard on Render
2. Navigate to "Environment" tab
3. Or use Render's file system (if available on your plan)

## Step 4: Verify Deployment

1. Wait for the build to complete (usually 5-10 minutes)
2. Check the logs for any errors
3. Visit your service URL (e.g., `https://chain-explorer.onrender.com`)
4. Test the RAG chatbot at `/query`

## Important Notes

### Build Time
- First build may take 10-15 minutes due to `sentence-transformers` and `torch` installation
- Subsequent builds are faster due to caching

### Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading to paid plan for always-on service

### Memory Considerations
- The RAG system loads models into memory
- Free tier has 512MB RAM limit
- If you encounter memory issues, consider:
  - Using smaller embedding models
  - Reducing number of workers in Procfile

### Environment Variables
Make sure to set:
- `SECRET_KEY`: A secure random string (Render can generate this)
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `False`

## Troubleshooting

### Build Fails
- Check logs for specific errors
- Ensure all dependencies in `requirements.txt` are correct
- Verify Python version in `runtime.txt` matches Render's support

### Service Won't Start
- Check `Procfile` syntax
- Verify `wsgi.py` is correct
- Check environment variables are set

### Out of Memory
- Reduce workers in Procfile: `--workers 1`
- Consider using smaller models
- Upgrade to paid plan

### Slow First Request
- This is normal on free tier (cold start)
- Consider using a paid plan for always-on service

## Monitoring

1. **Logs**: View real-time logs in Render dashboard
2. **Metrics**: Monitor CPU, memory, and request metrics
3. **Health Check**: The `/health` endpoint returns service status

## Updating Deployment

To update your deployment:

```bash
git add .
git commit -m "Update description"
git push origin main
```

Render will automatically detect changes and redeploy.

## Custom Domain (Optional)

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Follow DNS configuration instructions

---

**Your app should now be live!** 🚀


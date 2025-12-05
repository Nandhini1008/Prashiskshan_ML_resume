# Resume ATS Service - Quick Deployment Guide

## 🚀 Deploy to Render in 5 Minutes

### Step 1: Prepare Your Code

```bash
cd Prashiskshan_ml/resume
```

Verify these files exist:

- ✅ `Dockerfile`
- ✅ `render.yaml`
- ✅ `requirements.txt`
- ✅ `api_server.py`

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Add Resume ATS Service for Render deployment"
git push origin main
```

### Step 3: Deploy on Render

1. **Go to Render**: https://dashboard.render.com/
2. **Click**: "New +" → "Web Service"
3. **Connect**: Your GitHub repository
4. **Select**: The repository with this code
5. **Configure**:

   - Name: `resume-ats-service`
   - Environment: `Docker`
   - Root Directory: `Prashiskshan_ml/resume`
   - Dockerfile Path: `./Dockerfile`

6. **Add Environment Variables**:

   ```
   GOOGLE_API_KEY=your_key_here
   AI_GEMINI_API_KEY=your_key_here
   RUBRIC_GEMINI_API_KEY=your_key_here
   ```

7. **Click**: "Create Web Service"

### Step 4: Wait for Deployment

⏱️ Takes 5-10 minutes for first deployment.

### Step 5: Get Your API URL

After deployment completes:

```
https://resume-ats-service.onrender.com
```

### Step 6: Test Your API

```bash
# Health check
curl https://resume-ats-service.onrender.com/health

# API docs
open https://resume-ats-service.onrender.com/docs
```

### Step 7: Update Your Backend

In `Prashiskshan_backend/.env`:

```env
RESUME_SERVICE_URL=https://resume-ats-service.onrender.com
```

## 🧪 Local Testing (Optional)

### Build Docker Image

```bash
# Windows
docker-build.bat

# Linux/Mac
chmod +x docker-build.sh
./docker-build.sh
```

### Run Locally

```bash
docker run -p 8002:8002 --env-file .env resume-ats-service:latest
```

### Test Locally

```bash
curl http://localhost:8002/health
```

## 📡 API Usage

### Process Resume

```bash
curl -X POST https://resume-ats-service.onrender.com/process-resume \
  -F "file=@resume.pdf"
```

### Response Format

```json
{
  "success": true,
  "evaluation": {
    "overall_score": 85,
    "category_scores": {...},
    "strengths": [...],
    "weaknesses": [...]
  },
  "enhancements": {
    "original": {...},
    "recommended": {...}
  }
}
```

## 🔧 Troubleshooting

### Build Fails

```bash
# Test locally first
docker build -t resume-ats-service .
```

### Service Crashes

Check logs in Render Dashboard → Your Service → Logs

### Slow Response

Upgrade from Free to Starter tier ($7/month)

## 💰 Pricing

| Tier     | Cost   | RAM   | CPU | Best For    |
| -------- | ------ | ----- | --- | ----------- |
| Free     | $0     | 512MB | 0.1 | Testing     |
| Starter  | $7/mo  | 512MB | 0.5 | Development |
| Standard | $25/mo | 2GB   | 1.0 | Production  |

## 📚 Full Documentation

See `RENDER_DEPLOYMENT.md` for complete guide.

## ✅ Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Environment variables set
- [ ] Service deployed successfully
- [ ] Health check passes
- [ ] Backend updated with new URL
- [ ] Test resume processing works

## 🎉 Done!

Your Resume ATS Service is now live and ready to use!

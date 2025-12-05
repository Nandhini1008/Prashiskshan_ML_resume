# Resume ATS Service - Render Deployment Guide

## Overview

This guide explains how to deploy the Resume ATS Scoring Service to Render using Docker.

## Prerequisites

- Render account (free tier available)
- GitHub repository with this code
- Google Gemini API keys

## Deployment Methods

### Method 1: Automatic Deployment (Recommended)

#### Step 1: Push to GitHub

```bash
cd Prashiskshan_ml/resume
git add .
git commit -m "Add Resume ATS Service with Docker"
git push origin main
```

#### Step 2: Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the repository containing this code

#### Step 3: Configure Service

Render will auto-detect the `render.yaml` file. Verify settings:

- **Name**: `resume-ats-service`
- **Environment**: `Docker`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Dockerfile Path**: `./Dockerfile`
- **Docker Context**: `./`

#### Step 4: Set Environment Variables

In Render dashboard, add these environment variables:

```
GOOGLE_API_KEY=your_google_api_key_here
AI_GEMINI_API_KEY=your_ai_gemini_api_key_here
RUBRIC_GEMINI_API_KEY=your_rubric_gemini_api_key_here
PORT=8002
HOST=0.0.0.0
```

#### Step 5: Deploy

Click "Create Web Service" and wait for deployment (5-10 minutes).

### Method 2: Manual Deployment

#### Step 1: Create New Web Service

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Choose "Deploy an existing image from a registry" OR "Build and deploy from a Git repository"

#### Step 2: Configure Docker Build

- **Root Directory**: `Prashiskshan_ml/resume`
- **Dockerfile Path**: `./Dockerfile`
- **Docker Build Context**: `./`

#### Step 3: Set Environment Variables

Add the same environment variables as Method 1.

#### Step 4: Deploy

Click "Create Web Service".

## Service URLs

After deployment, your service will be available at:

```
https://resume-ats-service.onrender.com
```

### API Endpoints

#### Health Check

```bash
GET https://resume-ats-service.onrender.com/health
```

#### Process Resume

```bash
POST https://resume-ats-service.onrender.com/process-resume
Content-Type: multipart/form-data

file: <resume.pdf>
```

#### API Documentation

```
https://resume-ats-service.onrender.com/docs
```

## Integration with Backend

### Update Node.js Backend

In your `Prashiskshan_backend/.env`:

```env
RESUME_SERVICE_URL=https://resume-ats-service.onrender.com
```

### Example API Call (Node.js)

```javascript
const FormData = require("form-data");
const axios = require("axios");
const fs = require("fs");

async function processResume(pdfPath) {
  const form = new FormData();
  form.append("file", fs.createReadStream(pdfPath));

  const response = await axios.post(
    `${process.env.RESUME_SERVICE_URL}/process-resume`,
    form,
    {
      headers: form.getHeaders(),
      timeout: 60000, // 60 seconds
    }
  );

  return response.data;
}

// Usage
const result = await processResume("./resume.pdf");
console.log("ATS Score:", result.evaluation.overall_score);
console.log("Enhancements:", result.enhancements);
```

## Configuration

### Environment Variables

| Variable                | Required | Description           | Default |
| ----------------------- | -------- | --------------------- | ------- |
| `GOOGLE_API_KEY`        | Yes      | Google Gemini API key | -       |
| `AI_GEMINI_API_KEY`     | Yes      | AI Gemini API key     | -       |
| `RUBRIC_GEMINI_API_KEY` | Yes      | Rubric Gemini API key | -       |
| `PORT`                  | No       | Server port           | 8002    |
| `HOST`                  | No       | Server host           | 0.0.0.0 |

### Resource Requirements

**Free Tier (Starter)**:

- 512 MB RAM
- 0.1 CPU
- Suitable for development/testing

**Paid Tier (Standard)**:

- 2 GB RAM
- 1 CPU
- Recommended for production

## Monitoring

### Health Check

Render automatically monitors the `/health` endpoint.

### Logs

View logs in Render Dashboard:

1. Go to your service
2. Click "Logs" tab
3. Monitor real-time logs

### Metrics

Monitor in Render Dashboard:

- CPU usage
- Memory usage
- Request count
- Response times

## Troubleshooting

### Issue: Build Fails

**Solution 1**: Check Dockerfile syntax

```bash
docker build -t resume-ats .
```

**Solution 2**: Verify requirements.txt

```bash
pip install -r requirements.txt
```

### Issue: Service Crashes

**Solution**: Check logs in Render Dashboard

- Look for Python errors
- Verify environment variables are set
- Check memory usage

### Issue: Slow Response

**Solution**: Upgrade to paid tier

- Free tier has limited resources
- Consider caching results
- Optimize PDF processing

### Issue: API Key Errors

**Solution**: Verify environment variables

1. Go to Render Dashboard
2. Click service → "Environment"
3. Verify all API keys are set correctly

## Testing Deployment

### Test Health Endpoint

```bash
curl https://resume-ats-service.onrender.com/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "resume-processing",
  "components": {
    "ocr": "ready",
    "evaluator": "ready",
    "enhancer": "ready"
  }
}
```

### Test Resume Processing

```bash
curl -X POST https://resume-ats-service.onrender.com/process-resume \
  -F "file=@resume.pdf" \
  -H "Content-Type: multipart/form-data"
```

## Scaling

### Horizontal Scaling

Render supports multiple instances:

1. Go to service settings
2. Increase "Instance Count"
3. Load balancing is automatic

### Vertical Scaling

Upgrade instance type:

1. Go to service settings
2. Change "Instance Type"
3. Options: Starter, Standard, Pro

## Cost Estimation

### Free Tier

- **Cost**: $0/month
- **Limitations**:
  - 750 hours/month
  - Spins down after inactivity
  - Slower cold starts

### Paid Tier (Standard)

- **Cost**: ~$7/month
- **Benefits**:
  - Always on
  - Faster performance
  - More resources

## Security

### API Keys

- Never commit API keys to Git
- Use Render environment variables
- Rotate keys regularly

### CORS

Update `api_server.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "https://your-backend-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Rate Limiting

Consider adding rate limiting:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/process-resume")
@limiter.limit("10/minute")
async def process_resume(request: Request, file: UploadFile = File(...)):
    # ... existing code
```

## Backup & Recovery

### Database

No database required - stateless service.

### File Storage

Temporary files are cleaned up automatically.

### Configuration

Backup `render.yaml` and environment variables.

## CI/CD

### Auto-Deploy

Render automatically deploys on:

- Push to main branch
- Pull request merge
- Manual trigger

### Deploy Hooks

Get webhook URL from Render Dashboard:

```bash
curl -X POST https://api.render.com/deploy/srv-xxxxx?key=xxxxx
```

## Support

### Render Support

- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com/)
- [Render Status](https://status.render.com/)

### Service Issues

Check logs and metrics in Render Dashboard.

## Summary

✅ **Docker-based deployment** - Consistent environment
✅ **Auto-scaling** - Handles traffic spikes
✅ **Health monitoring** - Automatic restarts
✅ **Easy integration** - REST API for backend
✅ **Cost-effective** - Free tier available

Your Resume ATS Service is now production-ready on Render!

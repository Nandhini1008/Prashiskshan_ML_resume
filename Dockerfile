# Resume ATS Scoring Service - Optimized for Render Free Tier (512MB)
# Uses PyPDF2 only (no OCR) to fit in memory limits
FROM python:3.11-slim

WORKDIR /app

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8002

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.render.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./

# Create output directory
RUN mkdir -p output

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8002/health', timeout=5)" || exit 1

# Run application
CMD uvicorn api_server:app --host 0.0.0.0 --port ${PORT:-8002} --workers 1

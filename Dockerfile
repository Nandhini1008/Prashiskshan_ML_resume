# Resume ATS Scoring Service - Ultra-Optimized for Render Free Tier (512MB)
# Uses PyPDF2 only (no OCR) to fit in memory limits
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables for minimal memory usage
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8002 \
    PYTHONOPTIMIZE=2

# Install ONLY essential system dependencies (minimal footprint)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc/* \
    && rm -rf /usr/share/man/*

# Copy minimal requirements (NO OCR dependencies)
COPY requirements.render.txt requirements.txt

# Install Python dependencies with minimal footprint
RUN pip install --no-cache-dir --compile -r requirements.txt \
    && find /usr/local/lib/python3.11 -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find /usr/local/lib/python3.11 -type f -name '*.pyc' -delete \
    && find /usr/local/lib/python3.11 -type f -name '*.pyo' -delete

# Copy ONLY essential application files (no OCR directory to save space)
COPY api_server.py process_resume.py resume_evaluator.py resume_enhancer.py ./
COPY resume_pdf_generator.py simple_enhancer.py ./

# Create minimal directories
RUN mkdir -p output && chmod 755 output

# Expose port
EXPOSE 8002

# Minimal health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8002}/health', timeout=5)" || exit 1

# Run with single worker to minimize memory
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "1", "--log-level", "warning"]

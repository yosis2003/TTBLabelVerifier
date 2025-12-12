# Use lightweight python image
FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
# Create working directory
WORKDIR /app

# Install system dependencies (needed for google vision client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libc6 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .
COPY vision_key.json /app/vision_key.json

# Environment variable for Cloud Run
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port 8080 to Cloud Run
EXPOSE 8080

# Gunicorn will run server:app (Flask app named "app" in server.py)
CMD ["gunicorn", "server:app", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "1", \
     "--threads", "1", \
     "--timeout", "0", \
     "--log-level", "debug", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--capture-output"]



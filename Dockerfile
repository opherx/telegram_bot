# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies (including Pillow)
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for bot token (or pass via docker run)
ENV TOKEN=YOUR_BOT_TOKEN

# Command to run the bot
CMD ["python", "main.py"]

# Use Python 3.13 base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variable for token (or pass via docker run)
ENV TOKEN=YOUR_BOT_TOKEN

# Command to run the bot
CMD ["python", "main.py"]

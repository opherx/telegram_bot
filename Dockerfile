# Use Python 3.13 base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose environment variable via docker run or .env (DO NOT hardcode)
# ENV TOKEN=YOUR_BOT_TOKEN

# Command to run the bot
CMD ["python", "main.py"]

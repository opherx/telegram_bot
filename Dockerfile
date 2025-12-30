# Use Python 3.11 (compatible with PTB 20.x JobQueue)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# Expose port if your bot uses a web server (optional)
EXPOSE 8080

# Environment variable for your bot token
# In Railway, you can set RAILWAY_BOT_TOKEN in the Environment tab
ENV TOKEN=${RAILWAY_BOT_TOKEN}

# Run the bot
CMD ["python", "main.py"]

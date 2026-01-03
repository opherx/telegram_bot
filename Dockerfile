FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Telegram bot
CMD ["python", "bot.py"]


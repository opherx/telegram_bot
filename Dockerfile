# Use full Python 3.11 image
FROM python:3.11

WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies (PTB with job-queue + Pillow)
RUN pip install -r requirements.txt

# Persist demo.db outside container (volume mapping)
VOLUME ["/app/demo.db"]

# Run the bot
CMD ["python", "main.py"]

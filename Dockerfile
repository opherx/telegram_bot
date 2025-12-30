FROM python:3.13-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV TOKEN=YOUR_BOT_TOKEN
CMD ["python", "main.py"]

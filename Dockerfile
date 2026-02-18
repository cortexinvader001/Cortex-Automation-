FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    chromium chromium-driver curl unzip git xvfb \
    python3-tk python3-dev \
    fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 libasound2 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "-m", "app.main"]

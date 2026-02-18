FROM python:3.12-slim

# Install dependencies for Chromium + Xvfb
RUN apt-get update && apt-get install -y \
    chromium chromium-driver curl unzip git xvfb \
    fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 libasound2 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Start Xvfb automatically
CMD Xvfb :99 -screen 0 1920x1080x24 & export DISPLAY=:99 && python -m app.main

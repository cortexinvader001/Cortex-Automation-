FROM python:3.12-slim

# Install dependencies for Chromium
RUN apt-get update && apt-get install -y \
    chromium chromium-driver curl unzip git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "app.main"]

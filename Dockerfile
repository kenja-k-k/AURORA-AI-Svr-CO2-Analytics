FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl libffi-dev libssl-dev python3-dev \
    && rm -rf /var/lib/apt/lists/* \

COPY requirements.txt .


COPY . .

EXPOSE 50053

CMD ["python", "server.py"]

FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
EXPOSE 5001
CMD ["python", "-m", "flight_planner.app"]
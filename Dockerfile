# Use official Python slim image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies for PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy Python dependencies file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

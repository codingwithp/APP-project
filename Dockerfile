# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies for dlib (CMake, build tools, boost)
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt to container
COPY requirements.txt .

# Install Python dependencies including dlib
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code
COPY . .

# Expose port (if your app uses a port, change or remove this)
EXPOSE 8000

# Command to run your app (change as needed)
CMD ["python", "app.py"]

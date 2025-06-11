# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install \
    flask \
    opencv-python \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    ultralytics \
    mysql-connector-python \
    matplotlib \
    numpy \
    pandas \
    Pillow

# Expose Flask port
EXPOSE 5000

# Default command to run the app
CMD ["python", "app.py"]

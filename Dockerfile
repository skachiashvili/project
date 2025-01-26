# Use a slim base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgfortran5 \
    libopenblas64-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create the upload directory and set permissions
RUN mkdir -p /app/static/uploads && chmod 755 /app/static/uploads

# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies and clean up cache in a single RUN command
RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge && \
    rm -rf /root/.cache/pip

# Copy the rest of the application code
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=application.py

# Expose port 5000
EXPOSE 5000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "application:app"]
# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code and notebooks
COPY . ./

# Start the Flask app on container startup
CMD ["python", "scripts/run_all.py"]

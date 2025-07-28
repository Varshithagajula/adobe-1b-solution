FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential poppler-utils gcc

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu


# Copy model and app files
COPY model /app/model
COPY main.py .

# Create input/output folders
RUN mkdir -p /app/input /app/output

CMD ["python", "main.py"]

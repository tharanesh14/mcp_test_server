# Base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc curl

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set default port (optional for MCP over HTTP)
EXPOSE 8000

# Run the MCP server using HTTP transport (not stdio)
CMD ["python", "server.py", "--transport", "http"]

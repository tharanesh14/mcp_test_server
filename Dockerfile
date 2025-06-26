# Use a minimal Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose MCP server port
EXPOSE 8000

# Run MCP with HTTP transport
CMD ["python", "server.py", "--transport", "http"]

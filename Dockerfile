# Rose Looking Glass - Production Docker Image
FROM python:3.11-slim

LABEL maintainer="Rose Glass Community"
LABEL description="Rose Looking Glass v2.1 - Translation service for synthetic-organic intelligence"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY examples/ ./examples/
COPY tests/ ./tests/

# Create non-root user
RUN useradd -m -u 1000 roseglass && \
    chown -R roseglass:roseglass /app

USER roseglass

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the API server
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

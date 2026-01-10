FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY config.py chatbot.py api.py .

# Expose port for AgentCore HTTP protocol
EXPOSE 8080

# Run the application on AgentCore required port
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
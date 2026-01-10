# BaseballGo - AI Chatbot API

A conversational AI chatbot API powered by OpenAI and LangChain, designed for deployment on AWS Bedrock AgentCore Runtime.

## Features

- RESTful API with FastAPI
- AWS Bedrock AgentCore compatible
- Docker containerization
- ARM64 support for AWS deployment
- Secure API key management with environment variables
- Error handling for robust operation

## Prerequisites

- Python 3.12+ (avoid Python 3.14)
- OpenAI API key
- Docker (for containerization)
- AWS Account (for AgentCore deployment)

## Setup Instructions

### 1. Clone or Download the Repository

```bash
cd BaseballGo
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it starts with `sk-`)

### 5. Configure Environment Variables

Edit the `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
MODEL_NAME=gpt-4o-mini
```

## Usage

### Running Locally

```bash
# Start the FastAPI server
uvicorn api:app --host 0.0.0.0 --port 8080

# Or run directly
python api.py
```

The API will be available at `http://localhost:8080`

### Testing the API

```bash
# Test invocation endpoint
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'

# Health check
curl http://localhost:8080/ping
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ping` | GET | Health check |
| `/invocations` | POST | Chat with the AI |

### Request/Response Format

**Request:**
```json
{
  "message": "Your question here"
}
```

**Response:**
```json
{
  "response": "AI response here"
}
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t baseballgo .
```

### Run Docker Container

```bash
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=sk-your-key-here \
  -e MODEL_NAME=gpt-4o-mini \
  baseballgo
```

### Deploy to AWS ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build ARM64 image for AWS
docker buildx build --platform linux/arm64 \
  -t YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/baseballgo:latest \
  --push .
```

## Configuration

Environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `MODEL_NAME` - The OpenAI model to use (default: `gpt-4o-mini`)
  - Options: `gpt-4o-mini`, `gpt-4o`, `gpt-4`, etc.

## Project Structure

```
BaseballGo/
├── .env                    # Environment variables (not in git)
├── .gitignore              # Git ignore file
├── .dockerignore           # Docker ignore file
├── Dockerfile              # Docker container definition
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── CLAUDE.md               # Developer documentation
├── api.py                  # FastAPI REST API
├── chatbot.py              # Chatbot logic
└── config.py               # Configuration loading
```

## Architecture

1. **Configuration Loading** (`config.py`): Loads and validates environment variables
2. **Chatbot Logic** (`chatbot.py`): LangChain chain with OpenAI LLM
3. **API Layer** (`api.py`): FastAPI REST endpoints for AgentCore compatibility

**Note:** This chatbot does not maintain conversation history between requests. Each request is independent.

## AWS Bedrock AgentCore Deployment

This API is designed for AWS Bedrock AgentCore Runtime:

1. Build and push Docker image to ECR (see above)
2. Create AgentCore runtime agent pointing to your ECR image
3. Configure the agent to use port 8080
4. Test using AgentCore Test Sandbox

The `/ping` endpoint is used by AgentCore for health checks, and `/invocations` is the primary chat endpoint.

## Troubleshooting

### "OPENAI_API_KEY not found" error

Make sure you've created a `.env` file with your actual API key, or passed it as an environment variable to Docker.

### "Rate limit reached" error

You've exceeded your OpenAI API rate limit. Wait a few moments and try again, or upgrade your OpenAI plan.

### Import errors

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Docker build fails on Python 3.14

Use Python 3.12 instead. Python 3.14 lacks pre-built wheels for many packages.

## Future Enhancements

To add conversation history across container instances:
- Implement DynamoDB-based session storage
- Use Redis for caching chat history
- Add session ID to request/response flow

## Contributing

Feel free to submit issues or pull requests to improve the chatbot!

## License

This project is open source and available for educational purposes.
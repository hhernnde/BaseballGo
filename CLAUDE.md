# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BaseballGo is a conversational AI chatbot API powered by OpenAI and LangChain, designed for deployment on AWS Bedrock AgentCore Runtime.

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the FastAPI server locally
uvicorn api:app --host 0.0.0.0 --port 8080

# Or run directly
python api.py
```

### Testing Locally
```bash
# Test the API
curl -X POST http://localhost:8080/invocations -H "Content-Type: application/json" -d "{\"message\": \"Hello\"}"

# Health check
curl http://localhost:8080/ping
```

## Architecture

### Three-Module Structure

1. **config.py** - Configuration management
   - Loads environment variables from `.env`
   - Validates OpenAI API key presence and format
   - Provides configuration dictionary with `api_key` and `model_name`

2. **chatbot.py** - Chatbot logic
   - LangChain chain: `ChatPromptTemplate | ChatOpenAI`
   - Error handling for OpenAI rate limits and API errors

3. **api.py** - FastAPI REST API
   - AgentCore-compatible HTTP endpoints
   - Single global `Chatbot` instance initialized at startup

### Key Implementation Details

**LangChain Pattern**
- Uses `ChatPromptTemplate` with system + human message structure
- Chains prompt with LLM: `prompt | self.llm`
- Direct `.invoke()` call

**Configuration**
- Environment variables loaded via `python-dotenv`
- API key validation prevents placeholder values
- Default model: `gpt-4o-mini`

## Environment Setup

Requires `.env` file with:
```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini
AWS_ACCOUNT_ID=your-account-id
AWS_REGION=us-east-1
```

## Dependencies

Uses modern versions compatible with Python 3.12+:
- `langchain==0.3.17`
- `langchain-openai==0.2.14`
- `openai==1.59.8`
- `python-dotenv==1.0.1`
- `fastapi`
- `uvicorn`

Note: Avoid Python 3.14 as many packages lack pre-built wheels and require C++ compiler.

## Common Modifications

**Changing the system prompt**: Edit the system message in [chatbot.py:29](chatbot.py#L29) within `ChatPromptTemplate.from_messages()`

**Adjusting model parameters**: Modify temperature or other LLM parameters in [chatbot.py:20-25](chatbot.py#L20-L25)

## AWS Bedrock AgentCore Deployment

The API is configured for AWS Bedrock AgentCore Runtime compatibility using the HTTP protocol.

### AgentCore Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ping` | GET | Health check (returns HTTP 200) |
| `/invocations` | POST | Agent invocation |

Port: **8080** (required by AgentCore HTTP protocol)

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

### Deploy to ECR (ARM64)

Note: Replace AWS account ID and region with your own values.

```bash
# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Build and push ARM64 image
docker buildx build --platform linux/arm64 -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/baseballgo:latest --push .
```

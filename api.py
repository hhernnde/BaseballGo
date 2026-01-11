from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import Chatbot
from config import load_config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global chatbot instance
chatbot = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - initialize chatbot on startup."""
    global chatbot
    try:
        config = load_config()
        chatbot = Chatbot(config)
        logger.info("Chatbot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        raise
    yield


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AI Chatbot API",
    description="A conversational AI chatbot powered by OpenAI and LangChain",
    version="1.0.0",
    lifespan=lifespan
)


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str


class StatusResponse(BaseModel):
    """Response model for status endpoints."""
    status: str


@app.get("/ping", response_model=StatusResponse)
async def ping():
    """
    Health check endpoint for AgentCore Runtime.

    Returns:
        StatusResponse: Health status (HTTP 200)
    """
    return StatusResponse(status="healthy")


@app.post("/invocations", response_model=ChatResponse)
async def invocations(request: ChatRequest):
    """
    AgentCore Runtime invocation endpoint.

    Args:
        request: ChatRequest with message

    Returns:
        ChatResponse: The agent's response
    """
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        response = chatbot.send_message(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
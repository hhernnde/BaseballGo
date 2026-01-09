from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import ChatbotManager
from config import load_config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Chatbot API",
    description="A conversational AI chatbot powered by OpenAI and LangChain",
    version="1.0.0"
)

# Initialize chatbot manager on startup
manager = None


@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot manager on application startup."""
    global manager
    try:
        config = load_config()
        manager = ChatbotManager(config)
        logger.info("Chatbot manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot manager: {e}")
        raise


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    session_id: str


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

    This is the primary endpoint called by AWS Bedrock AgentCore to invoke the agent.

    Args:
        request: ChatRequest with message and optional session_id

    Returns:
        ChatResponse: The agent's response
    """
    if manager is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        response = manager.send_message(request.session_id, request.message)
        return ChatResponse(response=response, session_id=request.session_id)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/invocations/{session_id}", response_model=StatusResponse)
async def clear_session(session_id: str):
    """
    Clear conversation history for a specific session.

    Args:
        session_id: The session identifier to clear

    Returns:
        StatusResponse: Confirmation of cleared session
    """
    if manager is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")

    manager.clear_session(session_id)
    return StatusResponse(status="cleared")


@app.get("/sessions")
async def list_sessions():
    """
    List all active session IDs.

    Returns:
        dict: List of active sessions
    """
    if manager is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")

    return {"sessions": manager.list_sessions()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BaseballGo is a command-line conversational AI chatbot powered by OpenAI's API and LangChain. It maintains conversation history and provides an interactive terminal interface.

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
python main.py
```

### In-Chat Commands
- `/quit` or `/exit` - Exit the chatbot
- `/clear` - Clear conversation history
- `/help` - Show help message

## Architecture

### Three-Module Structure

1. **config.py** - Configuration management
   - Loads environment variables from `.env`
   - Validates OpenAI API key presence and format
   - Provides configuration dictionary with `api_key`, `model_name`, and `max_history`

2. **chatbot.py** - Core chatbot logic
   - Uses LangChain's modern `RunnableWithMessageHistory` pattern (not deprecated `ConversationChain`)
   - Manages conversation history with `InMemoryChatMessageHistory`
   - Implements sliding window memory by trimming messages when exceeding `max_history * 2`
   - Error handling for OpenAI rate limits and API errors

3. **main.py** - Entry point and interactive loop
   - Handles user input/output
   - Processes special commands (`/quit`, `/clear`, `/help`)
   - Displays formatted responses and error messages

### Key Implementation Details

**LangChain Pattern (Updated for 0.3.x)**
- Uses `ChatPromptTemplate` with `MessagesPlaceholder` for conversation history
- Chains prompt template with LLM using pipe operator: `prompt | self.llm`
- Wraps chain with `RunnableWithMessageHistory` for automatic history management
- Invokes with session configuration: `{"configurable": {"session_id": "default"}}`

**Memory Management**
- Manual history trimming in `send_message()` keeps last `max_history * 2` messages
- Each conversation turn creates 2 messages (user + AI)
- History is stored in `InMemoryChatMessageHistory` instance

**Configuration**
- Environment variables loaded via `python-dotenv`
- API key validation prevents placeholder values
- Default model: `gpt-4o-mini`
- Default history length: 10 turns

## Environment Setup

Requires `.env` file with:
```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini
MAX_HISTORY_LENGTH=10
```

## Dependencies

Uses modern versions compatible with Python 3.12+:
- `langchain==0.3.17`
- `langchain-openai==0.2.14`
- `openai==1.59.8`
- `python-dotenv==1.0.1`

Note: Avoid Python 3.14 as many packages lack pre-built wheels and require C++ compiler.

## Common Modifications

**Changing the system prompt**: Edit the system message in [chatbot.py:35](chatbot.py#L35) within `ChatPromptTemplate.from_messages()`

**Adjusting memory behavior**: Modify trimming logic in [chatbot.py:64-67](chatbot.py#L64-L67) within `send_message()`

**Adding new commands**: Extend command handling in [main.py:56-67](main.py#L56-L67) within the main loop

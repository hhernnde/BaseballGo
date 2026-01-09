# AI Chatbot with OpenAI and LangChain

A simple command-line conversational AI chatbot powered by OpenAI's API and LangChain. The chatbot maintains conversation history and provides an interactive terminal interface.

## Features

- Interactive command-line interface
- Conversation history with sliding window memory
- Multiple commands for controlling the chat experience
- Secure API key management with environment variables
- Error handling for robust operation

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Setup Instructions

### 1. Clone or Download the Repository

If you haven't already, navigate to the project directory:

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

Edit the `.env` file in the project root and replace the placeholder with your actual API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
MODEL_NAME=gpt-4o-mini
MAX_HISTORY_LENGTH=10
```

## Usage

### Running the Chatbot

```bash
python main.py
```

### Available Commands

Once the chatbot is running, you can use these commands:

- `/quit` or `/exit` - Exit the chatbot
- `/clear` - Clear conversation history
- `/help` - Show help message

### Example Conversation

```
You: Hello, my name is Alex
AI: Hello Alex! It's nice to meet you. How can I help you today?

You: What's my name?
AI: Your name is Alex, as you just told me!

You: /clear
Conversation history cleared.

You: What's my name?
AI: I don't know your name. Could you tell me?

You: /quit
Goodbye! Thanks for chatting.
```

## Configuration

You can customize the chatbot behavior by editing the `.env` file:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `MODEL_NAME` - The OpenAI model to use (default: `gpt-4o-mini`)
  - Options: `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`, etc.
- `MAX_HISTORY_LENGTH` - Number of conversation turns to remember (default: `10`)

## Project Structure

```
BaseballGo/
├── .env                    # Environment variables (not in git)
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── main.py                 # Entry point and chat loop
├── chatbot.py              # Core chatbot logic
└── config.py               # Configuration loading
```

## How It Works

1. **Configuration Loading** (`config.py`): Loads and validates environment variables
2. **Chatbot Logic** (`chatbot.py`): Integrates LangChain with OpenAI's API and manages conversation memory
3. **Main Loop** (`main.py`): Handles user input, displays responses, and processes commands

The chatbot uses LangChain's `ConversationBufferWindowMemory` to maintain a sliding window of recent conversation turns, preventing token limit issues while maintaining context.

## Troubleshooting

### "OPENAI_API_KEY not found" error

Make sure you've created a `.env` file and added your actual API key.

### "Rate limit reached" error

You've exceeded your OpenAI API rate limit. Wait a few moments and try again.

### Import errors

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Virtual environment issues

Make sure your virtual environment is activated before running the chatbot.

## Contributing

Feel free to submit issues or pull requests to improve the chatbot!

## License

This project is open source and available for educational purposes.
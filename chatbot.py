from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import openai


class Chatbot:
    """
    AI Chatbot powered by OpenAI and LangChain.
    Maintains conversation history using message history.
    """

    def __init__(self, config):
        """
        Initialize the chatbot with configuration.

        Args:
            config (dict): Configuration dictionary with api_key, model_name, and max_history
        """
        try:
            # Initialize OpenAI LLM
            self.llm = ChatOpenAI(
                model=config["model_name"],
                temperature=0.7,
                api_key=config["api_key"]
            )

            # Set up conversation memory
            self.chat_history = InMemoryChatMessageHistory()
            self.max_history = config["max_history"]

            # Create prompt template with message history
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful AI assistant. Have a natural conversation with the user."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])

            # Create chain with message history
            chain = prompt | self.llm

            self.chain = RunnableWithMessageHistory(
                chain,
                lambda session_id: self.chat_history,
                input_messages_key="input",
                history_messages_key="chat_history"
            )

        except Exception as e:
            raise RuntimeError(f"Failed to initialize chatbot: {str(e)}")

    def send_message(self, user_input):
        """
        Send a message to the chatbot and get a response.

        Args:
            user_input (str): The user's message

        Returns:
            str: The chatbot's response
        """
        try:
            # Trim history if it exceeds max_history
            messages = self.chat_history.messages
            if len(messages) > self.max_history * 2:  # *2 because each turn has user + AI message
                self.chat_history.messages = messages[-(self.max_history * 2):]

            # Invoke chain with message history
            response = self.chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "default"}}
            )

            return response.content

        except openai.RateLimitError:
            return "Error: Rate limit reached. Please try again later."

        except openai.APIError as e:
            return f"Error: API error occurred - {str(e)}"

        except Exception as e:
            return f"Error: Unexpected error - {str(e)}"

    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.chat_history.clear()


class ChatbotManager:
    """
    Manages multiple chatbot sessions for concurrent users.
    Each session gets its own Chatbot instance with separate conversation history.
    """

    def __init__(self, config):
        """
        Initialize the manager with configuration.

        Args:
            config (dict): Configuration dictionary passed to each Chatbot instance
        """
        self.config = config
        self.sessions = {}  # session_id -> Chatbot instance

    def get_or_create_session(self, session_id):
        """
        Get existing session or create a new one.

        Args:
            session_id (str): Unique identifier for the session

        Returns:
            Chatbot: The chatbot instance for this session
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = Chatbot(self.config)
        return self.sessions[session_id]

    def send_message(self, session_id, message):
        """
        Send a message to a specific session.

        Args:
            session_id (str): The session identifier
            message (str): The user's message

        Returns:
            str: The chatbot's response
        """
        chatbot = self.get_or_create_session(session_id)
        return chatbot.send_message(message)

    def clear_session(self, session_id):
        """
        Clear and remove a session.

        Args:
            session_id (str): The session to clear
        """
        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self):
        """
        List all active session IDs.

        Returns:
            list: List of active session IDs
        """
        return list(self.sessions.keys())
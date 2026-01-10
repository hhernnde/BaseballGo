from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import openai


class Chatbot:
    """
    AI Chatbot powered by OpenAI and LangChain.
    """

    def __init__(self, config):
        """
        Initialize the chatbot with configuration.

        Args:
            config (dict): Configuration dictionary with api_key and model_name
        """
        try:
            # Initialize OpenAI LLM
            self.llm = ChatOpenAI(
                model=config["model_name"],
                temperature=0.7,
                api_key=config["api_key"]
            )

            # Create simple prompt template (no history)
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful AI assistant."),
                ("human", "{input}")
            ])

            # Create chain
            self.chain = self.prompt | self.llm

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
            # Invoke chain
            response = self.chain.invoke({"input": user_input})
            return response.content

        except openai.RateLimitError:
            return "Error: Rate limit reached. Please try again later."

        except openai.APIError as e:
            return f"Error: API error occurred - {str(e)}"

        except Exception as e:
            return f"Error: Unexpected error - {str(e)}"

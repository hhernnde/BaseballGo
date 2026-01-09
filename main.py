from chatbot import Chatbot
from config import load_config
import sys


def print_welcome():
    """Display welcome message and instructions."""
    print("\n" + "=" * 50)
    print("   Welcome to the BaseballGo Chatbot!")
    print("=" * 50)
    print("\nCommands:")
    print("  /quit or /exit - Exit the chatbot")
    print("  /clear - Clear conversation history")
    print("  /help - Show this help message")
    print("\nStart chatting below!")
    print("-" * 50 + "\n")


def print_help():
    """Display help message."""
    print("\nAvailable commands:")
    print("  /quit or /exit - Exit the chatbot")
    print("  /clear - Clear conversation history")
    print("  /help - Show this help message")
    print()


def main():
    """Main chat loop."""
    try:
        # Load configuration
        config = load_config()

        # Display welcome message
        print_welcome()

        # Initialize chatbot
        try:
            chatbot = Chatbot(config)
        except RuntimeError as e:
            print(f"\nFailed to initialize chatbot: {e}")
            print("Please check your configuration and try again.")
            sys.exit(1)

        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                # Handle empty input
                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() in ["/quit", "/exit"]:
                    print("\nGoodbye! Thanks for chatting.\n")
                    break

                elif user_input.lower() == "/clear":
                    chatbot.clear_history()
                    print("\nConversation history cleared.\n")
                    continue

                elif user_input.lower() == "/help":
                    print_help()
                    continue

                # Send message to chatbot
                response = chatbot.send_message(user_input)
                print(f"\nAI: {response}\n")

            except KeyboardInterrupt:
                print("\n\nGoodbye! Thanks for chatting.\n")
                break

            except EOFError:
                print("\n\nGoodbye! Thanks for chatting.\n")
                break

    except ValueError as e:
        print(f"\nConfiguration Error: {e}\n")
        sys.exit(1)

    except Exception as e:
        print(f"\nUnexpected Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
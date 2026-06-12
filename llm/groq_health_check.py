from llm.groq_client import GroqClient


def main():

    client = GroqClient()

    response = client.generate(
        "Say Hello from Groq."
    )

    print("\nGroq Response:\n")
    print(response)


if __name__ == "__main__":
    main()
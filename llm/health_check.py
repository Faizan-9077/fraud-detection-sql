from llm.llama_client import LlamaClient


def main():
    print("=" * 60)
    print("LLaMA 3 API Health Check")
    print("=" * 60)

    try:
        client = LlamaClient()

        prompt = "Hello How are you?"

        result = client.generate(prompt)

        print("\nModel Response:")
        print(result)

        print("\nAPI Connection Successful")
        print("Health Check Completed")

    except Exception as e:
        print("\nHealth Check Failed")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
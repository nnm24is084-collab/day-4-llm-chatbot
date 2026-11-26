
import os
import csv
import anthropic
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MODEL = "claude-sonnet-4-5"

INPUT_PRICE = 3.00
OUTPUT_PRICE = 15.00

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    max_retries=3
)

conversation_history = []

if not os.path.exists("cost_log.csv") or os.path.getsize("cost_log.csv") == 0:
    with open("cost_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp", "model", "input_tokens",
            "output_tokens", "estimated_cost_usd"
        ])

print("Claude Streaming Chatbot")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        assistant_reply = ""

        print("Claude: ", end="", flush=True)

        with client.messages.stream(
            model=MODEL,
            max_tokens=500,
            messages=conversation_history
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                assistant_reply += text

            message = stream.get_final_message()

        conversation_history.append({
            "role": "assistant",
            "content": assistant_reply
        })

        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens

        cost = (
            input_tokens * INPUT_PRICE +
            output_tokens * OUTPUT_PRICE
        ) / 1_000_000

        with open("cost_log.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().isoformat(),
                MODEL,
                input_tokens,
                output_tokens,
                round(cost, 8)
            ])

        print("\nInput tokens:", input_tokens)
        print("Output tokens:", output_tokens)
        print("Estimated cost: $", round(cost, 8))

    except anthropic.APIError as error:
        print("\nAPI Error:", error)
        conversation_history.pop()

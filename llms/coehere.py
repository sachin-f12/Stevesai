import cohere

co = cohere.ClientV2(
    "kY2jKjtLWb7jPyCEHSmFsXFBeQr7aR6c6FvXonxO"
)  # Get your free API key here: https://dashboard.cohere.com/api-keys
response = co.chat(
    model="command-r-plus-08-2024",
    messages=[
        {
            "role": "user",
            "content": "I'm joining a new startup called Co1t today. Could you help me write a one-sentence introduction message to my teammates.",
        }
    ],
)

print(response.message.content[0].text)

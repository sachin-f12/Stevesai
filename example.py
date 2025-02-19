import openai

# Set your API key
#openai.api_key = "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"  # Prefer using environment variables instead of hardcoding

# Create a client
client = openai.OpenAI()

# Use the updated API method
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content":'Give me 10 indian boys names'}]
)

print(response.choices[0].message.content)

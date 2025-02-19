import openai

client = openai.OpenAI()

# Use the updated API method
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content":'Give me 10 indian boys names'}]
)

print(response.choices[0].message.content)

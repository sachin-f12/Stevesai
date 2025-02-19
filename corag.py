import cohere

co = cohere.ClientV2(
    "kY2jKjtLWb7jPyCEHSmFsXFBeQr7aR6c6FvXonxO"
)  # Get your free API key here: https://dashboard.cohere.com/api-keys

documents = [
    {
        "data": {
            "text": "Reimbursing Travel Expenses: Easily manage your travel expenses by submitting them through our finance tool. Approvals are prompt and straightforward."
        }
    },
    {
        "data": {
            "text": "Working from Abroad: Working remotely from another country is possible. Simply coordinate with your manager and ensure your availability during core hours."
        }
    },
    {
        "data": {
            "text": "Health and Wellness Benefits: We care about your well-being and offer gym memberships, on-site yoga classes, and comprehensive health insurance."
        }
    },
]
# Add the user query
query = "Are there health benefits?"

# Generate the response
response = co.chat(
    model="command-r-plus-08-2024",
    messages=[{"role": "user", "content": query}],
    documents=documents,
)

# Display the response
print(response.message.content[0].text)
if response.message.citations:
    for citation in response.message.citations:
        print(citation, "\n")

import cohere

co = cohere.ClientV2(
    "kY2jKjtLWb7jPyCEHSmFsXFBeQr7aR6c6FvXonxO"
) 
documents = [
    "Reimbursing Travel Expenses: Easily manage your travel expenses by submitting them through our finance tool. Approvals are prompt and straightforward.",
    "Working from Abroad: Working remotely from another country is possible. Simply coordinate with your manager and ensure your availability during core hours.",
    "Health and Wellness Benefits: We care about your well-being and offer gym memberships, on-site yoga classes, and comprehensive health insurance.",
    "Performance Reviews Frequency: We conduct informal check-ins every quarter and formal performance reviews twice a year.",
]
# Add the user query
query = "Are there fitness-related perks?"

# Rerank the documents
results = co.rerank(
    model="rerank-v3.5", query=query, documents=documents, top_n=4
)

for result in results.results:
    print(result)

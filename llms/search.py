
import cohere

co = cohere.ClientV2(
    "kY2jKjtLWb7jPyCEHSmFsXFBeQr7aR6c6FvXonxO"
)
# Define the documents
documents = [
    "Joining Slack Channels: Be sure to join relevant channels to stay informed and engaged.",
    "Finding Coffee Spots: For your caffeine fix, cross the street to the café for artisan coffee.",
    "Working Hours Flexibility: While our core hours are 9 AM to 5 PM, we offer flexibility to adjust as needed.",
]

# Embed the documents
doc_emb = co.embed(
    model="embed-english-v3.0",
    input_type="search_document",
    texts=documents,
    embedding_types=["float"],
).embeddings.float
# Add the user query
query = "Ways to connect with my teammates"

# Embed the query
query_emb = co.embed(
    model="embed-english-v3.0",
    input_type="search_query",
    texts=[query],
    embedding_types=["float"],
).embeddings.float

import numpy as np


# Compute dot product similarity and display results
def return_results(query_emb, doc_emb, documents):
    n = 2  # customize your top N results
    scores = np.dot(query_emb, np.transpose(doc_emb))[0]
    max_idx = np.argsort(-scores)[:n]

    for rank, idx in enumerate(max_idx):
        print(f"Rank: {rank+1}")
        print(f"Score: {scores[idx]}")
        print(f"Document: {documents[idx]}\n")


return_results(query_emb, doc_emb, documents)

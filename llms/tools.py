import cohere

co = cohere.ClientV2(
    "kY2jKjtLWb7jPyCEHSmFsXFBeQr7aR6c6FvXonxO"
)  # Get your free API key here: https://dashboard.cohere.com/api-keys
def get_weather(location):
    # Implement your tool calling logic here
    return [{"temperature": "20C"}]
    # Return a list of objects e.g. [{"url": "abc.com", "text": "..."}, {"url": "xyz.com", "text": "..."}]


functions_map = {"get_weather": get_weather}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "gets the weather of a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "the location to get weather, example: San Fransisco, CA",
                    }
                },
                "required": ["location"],
            },
        },
    },
]
messages = [
    {"role": "user", "content": "What's the weather in Toronto?"}
]

response = co.chat(
    model="command-r-plus-08-2024", messages=messages, tools=tools
)

if response.message.tool_calls:
    messages.append(
        {
            "role": "assistant",
            "tool_calls": response.message.tool_calls,
            "tool_plan": response.message.tool_plan,
        }
    )
    print(response.message.tool_calls)

import json

if response.message.tool_calls:
    for tc in response.message.tool_calls:
        tool_result = functions_map[tc.function.name](
            **json.loads(tc.function.arguments)
        )
        tool_content = []
        for data in tool_result:
            tool_content.append(
                {
                    "type": "document",
                    "document": {"data": json.dumps(data)},
                }
            )
            # Optional: add an "id" field in the "document" object, otherwise IDs are auto-generated
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": tool_content,
            }
        )
response = co.chat(
    model="command-r-plus-08-2024", messages=messages, tools=tools
)
print(response.message.content[0].text)
if response.message.citations:
    for citation in response.message.citations:
        print(citation, "\n")

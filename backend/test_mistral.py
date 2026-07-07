# test_mistral.py
from openai import OpenAI

client = OpenAI(
    api_key="ruJZ7qI3wWe839qcTrHbjEQJ5stlQYPg",
    base_url="https://api.mistral.ai/v1"
)

response = client.chat.completions.create(
    model="mistral-small-latest",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(response.choices[0].message.content)
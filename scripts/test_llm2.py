from openai import OpenAI

client = OpenAI(
    base_url="https://chat.kiconnect.nrw/api/v1",
    api_key="",
)

resp = client.chat.completions.create(
    model="openai-gpt-oss-120b",
    messages=[{"role": "user", "content": "Hello"}],
)
print(resp.choices[0].message.content)
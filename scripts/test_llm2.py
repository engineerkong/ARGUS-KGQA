import os
from openai import OpenAI

client = OpenAI(
    base_url="https://chat.kiconnect.nrw/api/v1",
    api_key=os.environ.get("KICONNECT_API_KEY", ""),
)

models = client.models.list()
for m in models.data:
    print(m.id)
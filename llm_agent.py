import requests
import json
from config import *


def call_llm(prompt):
    url = f"{ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    body = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))

    try:
        response.raise_for_status()
        print(response.json())  # 👈 This will show the real error
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("[ERROR]", response.status_code, response.text)
        raise e

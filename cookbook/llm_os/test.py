from root_server_ip import SERVER_IP

# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url=SERVER_IP, api_key="lm-studio")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

while True:
    completion = client.chat.completions.create(
        model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})
"""
import requests

base_url = SERVER_IP

endpoints = [
    "models",
    "generate",
    "chat/completions"
]

for endpoint in endpoints:
    url = f"{base_url}/{endpoint}"
    print(f"Testando endpoint: {url}")
    try:
        if endpoint == "models":
            response = requests.get(url)
        else:
            response = requests.post(url, json={"prompt": "test", "max_tokens": 5})
        print(response.status_code, response.json())
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")

"""
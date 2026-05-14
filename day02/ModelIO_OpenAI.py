# Please install OpenAI SDK first: `pip install openai`

import os

import dotenv
from openai import OpenAI
dotenv.load_dotenv()

# 最底层。---  python 原生自带的openai sdk 不属于于langchain框架中

client = OpenAI(
    # api_key=os.getenv("deepseek-api"),
    # base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello,你是谁"},
    ],
    stream=False
)

print(response.choices[0].message.content)
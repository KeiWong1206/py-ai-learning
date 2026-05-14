"""
模型参数演示
"""
import os

import dotenv
from langchain.chat_models import init_chat_model
dotenv.load_dotenv()
model = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    # api_key=os.getenv("deepseek-api"),
    # base_url="https://api.deepseek.com",
    temperature=0.0

)

# 3.调用模型
for x in range(3):
    print(model.invoke("写一句关于春天的词,14字以内").content)

import os
from typing import TypedDict, Annotated

import dotenv
from langchain.chat_models import init_chat_model
dotenv.load_dotenv()
llm = init_chat_model(
    # model="qwen3.5-flash",
    model="gpt-5.4-nano-2026-03-17",
    model_provider="openai",
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]

class AnimalList(TypedDict):  #说到底还是字典型
    animals: Annotated[list[Animal], "动物与表情列表"] # List<Animal>

#，由于你使用的模型（qwen3.5-flash 通过 OpenAI 兼容模式）对
# with_structured_output 的底层机制支持不完整，导致 LangChain 无法强制模型遵循字段名，此时必须在 prompt 中显式约束。
messages = [{"role": "user", "content": "任意生成三种动物，以及他们的 emoji"}]

llm_with_structured_output = llm.with_structured_output(AnimalList)
resp = llm_with_structured_output.invoke(messages)
print(resp)
print(type(resp))

'''
{'animals': [{'id': 1, 'name': '狮子', 'scientific_name': 'Panthera leo', 'emoji': '🦁'}, 
{'id': 2, 'name': '大熊猫', 'scientific_name': 'Ailuropoda melanoleuca', 'emoji': '🐼'}, 
{'id': 3, 'name': '海豚', 'scientific_name': 'Delphinidae', 'emoji': '🐬'}]}
<class 'dict'>

按理说应该报错，但它没有报错！
原因只有一个：
TypedDict 只是提示，LangChain 不会在运行时校验字段是否匹配！
'''



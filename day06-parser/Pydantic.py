import os
from typing import List
from pydantic import BaseModel, Field

import dotenv
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()

llm = init_chat_model(
    model="gpt-5.4-nano-2026-03-17",
    model_provider="openai",
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)



# ================= 关键修改：用 Pydantic，不要用 TypedDict =================
class Animal(BaseModel):
    animal: str = Field(description="动物名称")
    emoji: str = Field(description="动物对应的emoji表情")

class AnimalList(BaseModel):
    animals: List[Animal] = Field(description="动物与表情列表")

# ==========================================================================

messages = [{"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}]

# 结构化输出
# llm_with_structured_output = llm.with_structured_output(AnimalList)
llm_with_structured_output = llm.with_structured_output(AnimalList)

resp = llm_with_structured_output.invoke(messages)

print(resp)
print(type(resp))  # 现在是 <class '__main__.AnimalList'>
print(resp.animals[0].animal)  # 可以直接点属性！超级方便

'''
qwen：

animals=[Animal(animal='狮子', emoji='🦁'), Animal(animal='大象', emoji='🐘'), Animal(animal='企鹅', emoji='🐧')]
<class '__main__.AnimalList'>
狮子

opneai：
animals=[Animal(animal='猫', emoji='🐱'), Animal(animal='企鹅', emoji='🐧'), Animal(animal='狮子', emoji='🦁')]
<class '__main__.AnimalList'>
猫

'''
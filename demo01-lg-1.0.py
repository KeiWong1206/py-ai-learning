import dotenv
from langchain.chat_models import init_chat_model
from openai import base_url, api_key

dotenv.load_dotenv() #从配置文件中读取

model = init_chat_model(model_provider="openai",model="qwen3.5-flash")
res = model.invoke("你是谁")
print(res.content)

model2 = init_chat_model(model_provider="openai", #langchain里面没有qwen系列的，使用兼容的opnenai
                         model="qwen3.5-flash",
                         api_key="sk-58ab8ca0ddd2400fb615bdf377b3375e",
                         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                         )
res2 = model2.invoke("你是谁？")

print(res2.content)





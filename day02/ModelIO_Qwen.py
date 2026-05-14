#pip install langchain-community
#pip install dashscope
import dotenv
import os
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage
from openai import base_url

dotenv.load_dotenv()

# 纯tonyiqwen ---好像就没有url这个路径，智能使用官方平台的url
chatLLM = ChatTongyi(  #chattongyi进一步包装了openaisdk，如果不填写url或者key，那么默认调用ali官方平台的url与环境变量中的key
    model="qwen-plus",
    # dashscope_api_key=os.getenv("OPENAI_API_KEY"),
    # dashscope_base_url=os.getenv("OPENAI_BASE_URL"),
    streaming=True,
    # model_provider="openai"  # 这个就没必要写了，因为不管写什么都是调用的阿里平台的url
    # other params...
)
# 打印结果
print(chatLLM.invoke("你是谁"))

print("*" * 60)

res = chatLLM.stream([HumanMessage(content="你好，你是谁")], streaming=True)
for r in res:
    print("chat resp:", r.content)

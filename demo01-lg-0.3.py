from langchain_openai import ChatOpenAI

# demo0 --- 简单调用，使用langchain的包
from dotenv import load_dotenv
load_dotenv()
# 1、直接暴露apikey，写在代码当中
llm = ChatOpenAI(
    model="qwen3.5-flash"
)
# 🍒 最新版调用（一行搞定）
response = llm.invoke("你好") #
print(response) #大模型返回的元数据
print(type(response))
# 输出结果
print(response.content)
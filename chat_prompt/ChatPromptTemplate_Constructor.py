"""
使用ChatPromptTemplate构造方法直接实例化
实例化时需要传入messages: Sequence[MessageLikeRepresentation]
messages 参数支持如下格式：
	tuple 构成的列表，格式为[(role, content)]
	dict 构成的列表，格式为[{“role”:... , “content”:...}]
	Message 类构成的列表
"""
import dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.chat_models import init_chat_model
dotenv.load_dotenv()

# 第一种
chatPromptTemplate = ChatPromptTemplate(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}。"),
        ("human", "你能帮我做什么?"),
        ("ai", "我能开发很多{thing}。"),
        ("human", "{user_input}"),
    ]
)

# 第二种
chatPromptTemplate2 = ChatPromptTemplate(
    [
        {"role":"system", "content":"你是一个AI开发工程师，你的名字是{name}。"},
        {"role":"human", "content":"你能帮我做什么?"},
        {"role":"ai", "content":"我能开发很多{thing}。"},
        {"role":"human", "content":"{user_input}"},
    ]
)

# 第三种
chatPromptTemplate3 = ChatPromptTemplate(
    [
        SystemMessage(content="你是AI助手，你的名字叫{name}。"),
        HumanMessage(content="请问：{question}")
    ]
)



prompt = chatPromptTemplate.format_messages(
    name="小谷AI", thing="AI", user_input="7 + 5等于多少") #参数形式传递
print(prompt)
print(type(prompt)) # <class 'list'>

llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
print()
print("======================")

result = llm.invoke(prompt)
print(result)
print(type(result))
print(result.content)  # <class 'langchain_core.messages.ai.AIMessage'>
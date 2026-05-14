"""
可持续记忆（RunnableWithMessageHistory）
"""
import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory  # 内存型消息记录
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os
dotenv.load_dotenv()


# 设置本地模型
llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 定义全局的“会话存储”，用来保存每个 session 的聊天历史
#    （真实项目中可改为 Redis、SQLite 等）
store = {}

def get_session_history(session_id: str):
    """
    根据 session_id 获取对应的历史消息对象。 而不是和v1一样，一股脑的往内存history读取所有的历史消息。
    如果不存在则创建一个新的 InMemoryChatMessageHistory。
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()  # user-001、user-002
    return store[session_id]


# 定义 Prompt 模板
#     - system: 给模型设定角色
#     - MessagesPlaceholder: 历史消息将注入这里
#     - human: 当前用户输入
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的厨师，会根据上下文回答问题。"),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])


#构建基本链：Prompt → LLM → 输出解析
memory_chain = prompt | llm | StrOutputParser()

# -----------------------------------------------------
# 将链包装为支持记忆的版本
with_history = RunnableWithMessageHistory(
    memory_chain,  # 原始链
    get_session_history,       # 获取历史函数，注意会根据会话id来读取对应的历史记录。
    input_messages_key="question",  # 对应 prompt 输入的 key
    history_messages_key="history", # 对应 MessagesPlaceholder 的变量名
)

# -----------------------------------------------------
# 模拟一个会话，用 session_id 区分不同用户
cfg = {"configurable": {"session_id": "user-001"}}

# 模拟一个会话，用 session_id 区分不同用户
cfg2 = {"configurable": {"session_id": "user-002"}}

# 第一次提问：告诉模型“我叫张三”
print("用户：我叫张三。")
print("AI：", with_history.invoke({"question": "我叫张三。"}, cfg))

# 第二次提问：让模型回忆前面的对话

print("\n 用户：我叫什么？")
print("AI：", with_history.invoke({"question": "我叫什么？"}, cfg2)) #使用不同的sessionid，读不到历史对话呢。

print(store)

'''
{'user-001': InMemoryChatMessageHistory(messages=[HumanMessage(content='我叫张三。', additional_kwargs={}, response_metadata={}), 
AIMessage(content='你好呀，张三！👋 很高兴认识你！\n\n我是你的厨师朋友。既然你已经到了我的“厨房”里，那以后就是熟人了！不管是想学一道拿手好菜，
还是不知道今晚吃什么烦恼，都可以随时告诉我哦。😋\n\n今天厨房里有什么特别安排吗？是准备大展厨艺，还是需要我推荐个食谱给你解解馋？', 
additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[])]), 
'user-002': InMemoryChatMessageHistory(messages=[HumanMessage(content='我叫什么？', additional_kwargs={}, 
response_metadata={}), AIMessage(content='哎呀，这可把我这位大厨难住啦！😅\n\n因为我们刚刚开始交流，我还不知道您的名字呢，
就像菜单上还没写下今日的“主厨推荐人”一样。不过没关系！我很希望能知道该怎么称呼您。\n\n
如果您愿意告诉我，我会把它当作最珍贵的“独家秘方”记在心里，以后就像对待一道好菜一样亲切地称呼您！👨
\u200d🍳\n\n那……请问该怎么称呼您呢？或者，今天有什么想聊聊的美食话题吗？🥘', additional_kwargs={}, 
response_metadata={}, tool_calls=[], invalid_tool_calls=[])])}
'''



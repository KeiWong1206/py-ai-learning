"""
可持续记忆（RunnableWithMessageHistory）
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from loguru import logger
import os
dotenv.load_dotenv()


# 设置本地模型
llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 定义 Prompt
prompt = ChatPromptTemplate.from_messages([
    # 用于插入历史消息
    MessagesPlaceholder(variable_name="history"), #历史对话站位
    ("human", "{input}") #human message就行
])

parser = StrOutputParser()
# 构建处理链：将提示词模板、语言模型和输出解析器组合
chain = prompt | llm | parser
# 创建内存聊天历史记录实例，用于存储对话历史
history = InMemoryChatMessageHistory()
# 创建带消息历史的可运行对象，用于处理带历史记录的对话
runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda session_id: history,  #都是同一个history对象
    input_messages_key="input",  # 指定输入键。
    history_messages_key="history"  # 指定历史消息键。 告诉langchain 提示词模版中的历史对话站位key是history，把从内
    #内存中读取到的历史消息，填充到history站位符哪里就可以。
)
# 清空历史记录
history.clear()
# 配置运行时参数，设置会话ID,之前是没有的，现在要根据不同的对话id选择历史对话。
config = RunnableConfig(configurable={"session_id": "user-001"})

logger.info(runnable.invoke({"input": "我叫张三，我爱好学习。"}, config))
logger.info(runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config))
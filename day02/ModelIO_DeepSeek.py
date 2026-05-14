import os

import dotenv
from langchain_deepseek import ChatDeepSeek
dotenv.load_dotenv()

# 初始化 deepseek
# 相当于独家的deepseek封装 ，底层依旧是封装最原生的openai sdk
# 但是调用地址换成了deepseek的官方api url 如果是使用第三方，那么就没用
# 给学生们看看ChatDeepSeek类的源码，解释为什么不写调用地址,chat_modesl.py源码第176行
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    # max_retries=2,
    # api_key=os.getenv("OPENAI_API_KEY"),
    # base_url=os.getenv("OPENAI_BASE_URL"),
)


# 打印结果
print(model.invoke("你是谁？"))
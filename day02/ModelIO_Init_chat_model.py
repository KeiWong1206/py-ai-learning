# 1.导入依赖
import os

import dotenv
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()
# 最新1.0版本的最上层的封装，相当于自己填写url（代理，或者原厂），自己确定model名称
# 2.实例化模型
model = init_chat_model(
    model="deepseek-chat",
    model_provider="openai"  #这个api key只支持openai 兼容协议，所有的厂商几乎都兼容
    # api_key=os.getenv("deepseek-api"),
    # base_url="https://api.deepseek.com"
)

# 3.调用模型
print(model.invoke("你是deepseek吗？").content) #纯文本输入
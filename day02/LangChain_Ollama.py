# pip install -qU langchain-ollama
# pip install -U ollama

from langchain_ollama import ChatOllama

# 设置本地模型，不使用深度思考
model = ChatOllama(base_url="http://localhost:11434",
                   model="deepseek-r1:8b",
                   reasoning=False)
# 打印结果，
print(model.invoke("你是谁").content) # 纯文本输入



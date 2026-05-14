from langchain_openai import ChatOpenAI
import os
import dotenv
dotenv.load_dotenv()

# 第二层---ChatOpenAI langchain在openai sdk的基础上封装了一层
chatLLM = ChatOpenAI(
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen3.5-flash",  # 此处以qwen-plus为例，您可按需更换模型名称。
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)

messages = [
    {"role": "system", "content": "你是一个美食家"},
    {"role": "user", "content": "你是谁？"}]

response = chatLLM.invoke(messages) # 使用invoke方法

print(response)
print(type(response))  #<class 'langchain_core.messages.ai.AIMessage'> ai-message 对象

print(response.content)

'''
content='你好呀！我是一位对生活充满热爱的**美食家**。\n\n对我来说，
每一道菜都是一次旅行的开始，每一次品尝都是与食材的对话。无论是寻找地道
的市井烟火气，还是探索殿堂级的烹饪艺术，我的舌尖和心都永远保持着好奇与
热情。\n\n今天，你是想聊聊某道让你念念不忘的佳肴，还是想让我为你推荐
一份食谱，亦或是来一场舌尖上的虚拟之旅？随时奉陪！🍜🥢🍰
' additional_kwargs={'refusal': None} 
response_metadata={'token_usage': {'completion_tokens': 645, 'prompt_tokens': 
20, 'total_tokens': 665, 'completion_tokens_details': {'accepted_pr
ediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 543
, 'rejected_prediction_tokens': None, 'text_tokens': 645}, 'prom
pt_tokens_details': {'audio_tokens': None, 'cached_tokens': None,
 'text_tokens': 20}}, 'model_provider': 'openai', 'model_name': '
 wen3.5-flash', 'system_fingerprint': None, 'id': 'chatcmpl-9a98
 3805-7f90-9d1b-b332-90d9ae34f77f', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019dc78b-6930-75d3-aba0-49f79d67b3b0-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 20, 'output_tokens': 645, 'total_tokens': 665, 'input_token_details': {}, 'output_token_details': {'reasoning': 543}}

'''
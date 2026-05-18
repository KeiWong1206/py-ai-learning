import os

import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputKeyToolsParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger
from QueryWeatherTool import get_weather,get_alert

dotenv.load_dotenv()

# 初始化大语言模型实例
llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 将模型与工具绑定，使其能够调用 get_weather 工具
llm_with_tools = llm.bind_tools([get_weather,get_alert])

# 创建解析器，用于提取大模型返回的 工具调用指令结果中的 JSON 数据，key指定工具名，有可能有多个工具，only，防止多个参数。主要是要得到：'args': {'city': '北京'},
parser = JsonOutputKeyToolsParser(key_name=get_weather.name, first_tool_only=True)

# print(llm.day03-invoke("你好请问北京天气怎么样").content)
# res = llm_with_tools.day03-invoke("你好， 请问北京的天气怎么样？")
# print(res.tool_calls)
# print(res)
'''
[{'name': 'get_weather', 'args': {'city': '北京'}, 'id': 'call_bd85f9220ab04948b8a40d41', 'type': 'tool_call'}]

content='' additional_kwargs={'refusal': None} response_metadata=
{'token_usage': {'completion_tokens': 73, 'prompt_tokens': 292, 'total_tokens': 
365, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': 
None, 'reasoning_tokens': 43, 'rejected_prediction_tokens': None, 'text_tokens': 73}, 
'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': None, 'text_tokens': 292}},
 'model_provider': 'openai', 'model_name': 'qwen3.5-flash', 'system_fingerprint': None, 'id': 
 'chatcmpl-d4b3e232-35b2-9d99-84e2-ed4e389fbe4b', 'finish_reason': 'tool_calls', 'logprobs': None} 
 id='lc_run--019e103e-5582-7c72-b25a-c7e28d44b41b-0' tool_calls=[{'name': 'get_weather', 
 'args': {'city': '北京'}, 'id': 'call_bd85f9220ab04948b8a40d41', 'type': 'tool_call'}] 
 invalid_tool_calls=[] usage_metadata={'input_tokens': 292, 'output_tokens': 73, 'total_tokens': 
 365, 'input_token_details': {}, 'output_token_details': {'reasoning': 43}}
'''


# 构建工具调用链：模型 -> 解析器 -> 调用天气工具
# get_weather_chain = llm_with_tools | get_weather # 这样不行，无法解析调用工具指令


get_weather_chain = llm_with_tools | parser | get_weather #请求大模型，大模型返回调用工具参数，调用工具获取结果
print(get_weather_chain.invoke("你好， 请问北京的天气怎么样？")) #这里成功返回tool的原始json数据：
'''
{
  "城市": "北京",
  "实时温度(℃)": "28",
  "天气状况": "Sunny",
  "风速(km/h)": "12",
  "湿度(%)": "35"
}
'''


# 定义输出提示模板，将 JSON 天气数据转换为自然语言描述
output_prompt = PromptTemplate.from_template(
    """你将收到一段 JSON 格式的天气数据{weather_json}，请用简洁自然的方式将其转述给用户。
    以下是天气 JSON 数据：
    请将其转换为中文天气描述，例如：
    “北京现在天气：多云，气温 28℃，体感有点闷热（约 32℃），湿度 75%，微风（东南风 2 米/秒），
    能见度很好，大约 10 公里。建议穿短袖短裤。适合做户外运动。"
    """
)
#
# # 创建字符串输出解析器
output_parser = StrOutputParser()
#
# # 构建最终输出链：提示模板 -> 模型 -> 输出解析器
output_chain = output_prompt | llm | output_parser #output接收上面返回的json数据，放{「weather_json:xx}(构建参数)当中
#
# # 构建完整的处理链：天气查询链 ->将天气数据包装为字典格式 -> 输出链
full_chain = get_weather_chain | (lambda x: {"weather_json": x}) | output_chain #把调用工具的返回结果，封装为字典参数传入
#新的prompt，然后执行后面的链。
#
#这里还没后引入agent，所以是先使用get_weather_chain ，传入问题"请问北京今天的天气如何？"，
# #然后大模型识别问题，还有tool工具，返回调用调用工具的json格式，langchain执行调用返回结果给parser进行解析
#
# # 执行完整链路，查询上海天气并打印结果
result = full_chain.invoke("请问广州今天的天气如何？")
logger.info(result)


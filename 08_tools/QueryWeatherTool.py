from langchain_core.tools import tool
import json
import os
import httpx


# @tool
# def get_weather(loc):
#     """
#     查询即时天气函数
#
#     :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
#                 注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，
#                 则 loc 参数需要输入 'Beijing'/'shanghai'。
#     # :return: OpenWeather API 查询即时天气的结果。具体 URL 请求地址为：
#     #          https://home.openweathermap.org/users/sign_in。
#     #          返回结果对象类型为解析之后的 JSON 格式对象，并用字符串形式进行表示，
#     #          其中包含了全部重要的天气信息。
#     # """
    # # Step 1. 构建请求 URL
    # url = "https://api.openweathermap.org/data/2.5/weather"
    #
    # # Step 2. 设置查询参数，包括城市名、API Key、单位和语言
    # params = {
    #     "q": loc,
    #     # "appid": os.getenv("OPENWEATHER_API_KEY"),  # 从环境变量中读取 API Key
    #     "appid": "c60b8ff8e22e196a77a841152e032a3a",  # 从环境变量中读取 API Key
    #     "units": "metric",  # 使用摄氏度
    #     "lang": "zh_cn"  # 输出语言为简体中文
    # }
    #
    # # Step 3. 发送 GET 请求获取天气数据
    # response = httpx.get(url, params=params, timeout=30)
    #
    # # Step 4. 解析响应内容为 JSON 并序列化为字符串返回
    # data = response.json()
    # #print(json.dumps(data))
    # return json.dumps(data)
@tool
def get_alert(city: str) -> str:
    """
    查询是否有台风预警
    :param city:
    :return:
    """
    return f"{city}没有台风预警"

@tool
def get_weather(city: str):
    """
    查询【当天实时天气】
    :param city: 城市中文名 例如：北京、上海、广州
    """
    url = f"https://wttr.in/{city}?format=j1&lang=zh"
    try:
        resp = httpx.get(url, timeout=15)
        data = resp.json()
        current = data["current_condition"][0]

        # 只保留 100% 一定存在的字段，不报错版本
        result = {
            "城市": city,
            "实时温度(℃)": current["temp_C"],
            "天气状况": current["weatherDesc"][0]["value"],
            "风速(km/h)": current["windspeedKmph"],
            "湿度(%)": current["humidity"]
        }

        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"天气查询失败：{str(e)}"

# 测试
# result = get_weather.day03-invoke("shanghai")
# result = get_weather.day03-invoke("beijing")
# print(result)


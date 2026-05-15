# 方式2：使用 from_template 方法实例化提示词模板
import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
dotenv.load_dotenv()

# 创建一个PromptTemplate对象，用于生成格式化的提示词模板
# 模板包含两个占位符：{role}表示角色，{question}表示问题
template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")

# 使用指定的角色和问题参数来格式化模板，生成最终的提示词字符串
# role: 工程师角色描述
# question: 具体的技术问题
prompt = template.format(role="python开发",question="快速排序怎么写？")

# 输出生成的提示词
print(prompt)
print(type(prompt))

print("\n\n")

# 使用 from_template 方法实例化提示词模板
template = PromptTemplate.from_template("请给我一个关于{topic}的{type}解释。")
# 使用模板生成提示
prompt = template.format(topic="祖父悖论",type="详细")
print(prompt)  # 请给我一个关于量子力学的详细解释。



model = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    # api_key=os.getenv("aliQwen-api"),
    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# format方法，参数，获取的prompt是string类型

res = model.invoke(prompt)

print(res.content)


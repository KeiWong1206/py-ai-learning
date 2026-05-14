import dotenv
from langchain.chat_models import init_chat_model

import os

model = init_chat_model(model_provider="openai",
                        model="qwen3.5-flash",
                        openai_key=os.environ["OPENAI_KEY"],
                        openai_url=os.environ["OPENAI_URL"],)
res = model.invoke("今天天气怎么样？")
print(res.content)
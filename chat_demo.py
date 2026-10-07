import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()                      # 去读 .env 文件，把里面的配置加载进来
api_key = os.getenv("DEEPSEEK_API_KEY")   # 从环境配置里取出 key

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
print("key 前几位:", api_key[:8])
print("key 长度:", len(api_key))
messages = [
    {"role": "user", "content": "你好，请用一句话介绍你自己"}
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)

print(response.choices[0].message.content)
# 把第一轮的用户提问和模型回答都记进历史
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# 第二轮：追问，看她记不记得自己是谁
messages.append({"role": "user", "content": "你刚才说你是谁？"})

response2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)

print("--- 第二轮回答 ---")
print(response2.choices[0].message.content)
print(response.usage)
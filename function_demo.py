import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


# 这就是"真函数"——将来真正被执行的代码
def get_weather(city: str) -> str:
    # 假数据，不用真去查（现在重点是流程，不是数据）
    fake_data = {
        "北京": "晴，22度，微风",
        "上海": "多云，25度，东南风3级",
        "广州": "雷阵雨，30度，湿度大",
    }
    return fake_data.get(city, f"没有{city}的数据")


# 这是给模型看的"说明书"——用 JSON 格式描述有哪些工具、参数是什么
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的实时天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海",
                    }
                },
                "required": ["city"],
            },
        },
    }
]

messages = [{"role": "user", "content": "北京今天天气怎么样？"}]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
)

print("=== 模型返回的原始内容 ===")
print(response.choices[0].message)
print()
print("=== 它想调的函数 ===")
print(response.choices[0].message.tool_calls[0].function.name)
print()
print("=== 它想传的参数 ===")
print(response.choices[0].message.tool_calls[0].function.arguments)

# ③ 把模型给的 JSON 字符串解析成真正的字典
args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
print("解析后的参数:", args)

# 真正执行函数
tool_result = get_weather(args["city"])
print("工具执行结果:", tool_result)

# ④ 把"模型的调用请求"和"工具的执行结果"都追加进历史
messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": response.choices[0].message.tool_calls[0].id,
    "content": tool_result,
})

# ⑤ 再调一次，这次模型能看到工具返回的真实数据
final = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
)

# ⑥ 最终回答
print()
print("=== 最终回答 ===")
print(final.choices[0].message.content)

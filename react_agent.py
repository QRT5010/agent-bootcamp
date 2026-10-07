import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


# ========== 工具 1：查天气 ==========
def get_weather(city: str) -> str:
    fake_data = {
        "北京": "22度",
        "上海": "25度",
        "广州": "30度",
    }
    return fake_data.get(city, f"没有{city}的数据")


# ========== 工具 2：算数 ==========
def calculate(expression: str) -> str:
    try:
        result = eval(expression)      # 让 Python 直接算这个表达式
        return str(result)
    except Exception as e:
        return f"计算出错: {e}"


# ========== 给模型看的说明书 ==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气温度",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如：北京"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算一个数学表达式，如 '25 - 22'",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式，如 '25 - 22'"},
                },
                "required": ["expression"],
            },
        },
    },
]

# ========== ReAct 主循环 ==========
question = "北京和上海的温差是多少？"
messages = [{"role": "user", "content": question}]

print(f"问题：{question}")
print("=" * 40)

step = 0                             # 记步数，防止死循环
while True:
    step += 1
    print(f"\n--- 第 {step} 轮思考 ---")

    # ① 问模型：现在该怎么办？
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
    )
    msg = response.choices[0].message

    # ② 模型想调工具吗？
    if msg.tool_calls:
        # 先把模型这条消息存进历史（它包含所有的 tool_calls）
        messages.append(msg)

        # 遍历它请求的每一个工具调用
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"模型决定调用：{func_name}，参数：{args}")

            # 执行
            if func_name == "get_weather":
                result = get_weather(args["city"])
            elif func_name == "calculate":
                result = calculate(args["expression"])
            else:
                result = f"未知工具：{func_name}"

            print(f"执行结果：{result}")

            # 每个请求都要给它一个对应的 tool 消息
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

        # 防死循环：最多 10 轮
        if step >= 10:
            print("达到最大步数，强制停止")
            break

    else:
        # 没有 tool_calls = 它要直接说话了
        print("\n" + "=" * 40)
        print("最终回答：")
        print(msg.content)
        break

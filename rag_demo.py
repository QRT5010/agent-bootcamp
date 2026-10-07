# 假装这是一份"学校规章制度文档"，被切成了 6 段
DOCUMENTS = [
    "学生请假需要提前向辅导员提交书面申请，经批准后方可离校。病假需附医院证明。",
    "图书馆开放时间为每天早上八点至晚上十点，周末照常开放，寒暑假另行通知。",
    "学生宿舍每晚十一点断电断网，考试周可申请延长至凌晨一点。",
    "补考安排在每学期开学后第二周进行，补考成绩最高按六十分计入绩点。",
    "校园卡丢失后应立即到一卡通服务中心挂失，补办工本费二十元。",
    "研究生申请学位论文答辩，需先修满规定学分并完成开题报告。",
]


import os
import chromadb
from fastembed import TextEmbedding
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------- 1. 向量化模型 ----------
embed_model = TextEmbedding(model_name="BAAI/bge-small-zh-v1.5")

# ---------- 2. 建 Chroma 库 ----------
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="school_rules")

# 先清空旧的（避免重复运行越堆越多）
existing = collection.get()
if existing["ids"]:
    collection.delete(ids=existing["ids"])

# 把 6 条规章全部向量化并入库
vectors = list(embed_model.embed(DOCUMENTS))          # 生成器 → 列表
collection.add(
    ids=[f"doc_{i}" for i in range(len(DOCUMENTS))],
    documents=DOCUMENTS,
    embeddings=[v.tolist() for v in vectors],
)
print(f"入库完成，共 {len(DOCUMENTS)} 条")


# ---------- 3. LLM 客户端 ----------
llm = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

def ask(question, top_k=3):
    # --- Retrieval：检索 ---
    q_vec = list(embed_model.embed([question]))[0].tolist()
    result = collection.query(query_embeddings=[q_vec], n_results=top_k)
    hits = result["documents"][0]                      # 命中原文列表

    # --- Augmented：拼提示词 ---
    context = "\n".join(hits)
    prompt = f"""你是一个学校规章制度助手。
请严格根据下面提供的资料回答问题，不要编造。
如果资料里找不到答案，就回答"资料里没有相关规定"。

【资料】
{context}

【问题】{question}"""

    # --- Generation：生成 ---
    resp = llm.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,                                  # 0 = 尽量不给它发挥空间
    )
    return resp.choices[0].message.content, hits

# ---------- 4. 交互式问答 ----------
print("=" * 50)
print("学校规章问答助手（输入 exit 退出）")
print("=" * 50)

while True:
    question = input("\n你问：").strip()

    # 空输入跳过
    if not question:
        continue

    # 太短的输入跳过（少于 2 个字符不算问题）
    if len(question) < 2:
        print("（输入太短，请说完整一点）")
        continue


    # 退出命令
    if question.lower() in ("exit", "quit", "q"):
        print("再见！")
        break

    answer, hits = ask(question)
    print(f"\n[检索命中 {len(hits)} 条]")
    print(f"答：{answer}")

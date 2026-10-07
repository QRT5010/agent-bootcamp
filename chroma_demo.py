from fastembed import TextEmbedding
import chromadb

# 1. 加载向量化模型
model = TextEmbedding(model_name="BAAI/bge-small-zh-v1.5")

# 2. 准备语料（假装这是从某个文档里切出来的几段）
documents = [
    "今天天气真好",
    "外面阳光明媚",
    "我喜欢吃火锅",
]

# 3. 建一个本地向量库，建一个集合（相当于数据库里的"表"）
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="demo")

# 4. 把语料变成向量，存进去
vectors = [v.tolist() for v in model.embed(documents)]

collection.add(
    ids=["doc1", "doc2", "doc3"],      # 每段的唯一编号
    documents=documents,               # 原文
    embeddings=vectors,                # 向量
)

print("库里现在有几条:", collection.count())

# 5. 查询：问一句话，找出语义最接近的
query = "外面出太阳了，心情很好"
query_vector = list(model.embed([query]))[0].tolist()

results = collection.query(
    query_embeddings=[query_vector],
    n_results=2,                       # 只返回最像的 2 条
)

print()
print("查询:", query)
print("最相关的 2 条:")
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"  {doc}   (距离: {dist:.4f})")

from fastembed import TextEmbedding

# 加载中文向量化模型（第一次运行会自动下载模型，约 95MB）
model = TextEmbedding(model_name="BAAI/bge-small-zh-v1.5")

# 要变成向量的三句话
texts = ["今天天气真好", "外面阳光明媚", "我喜欢吃火锅"]

# 变成向量
vectors = list(model.embed(texts))

print("一共处理了几句话:", len(vectors))
print("每句话变成多少个数字:", len(vectors[0]))
print()
print("第 1 句话向量的前 10 个数字:")
print(vectors[0][:10].tolist())


import numpy as np


def cosine(a, b):
    """算两个向量的余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


v1, v2, v3 = vectors[0], vectors[1], vectors[2]

print()
print("=" * 40)
print("两两相似度：")
print(f"天气真好 vs 阳光明媚 : {cosine(v1, v2):.4f}")
print(f"天气真好 vs 吃火锅   : {cosine(v1, v3):.4f}")
print(f"阳光明媚 vs 吃火锅   : {cosine(v2, v3):.4f}")

# agent-bootcamp

> 8 天从零手写 LLM / Agent 应用 —— 一份"不用框架、先拆开看"的学习仓库。

这个仓库记录了我从**编程零基础**到能自己写出一个 RAG 问答系统的全过程。所有代码**都不依赖 LangChain 等框架**，用最原始的方式（直接调 API、手搓循环）把每一层拆开看清，之后再去看框架就知道它在封装什么。

## 这里有什么

| 文件 | 是什么 | 用到的关键概念 |
|---|---|---|
| `main.py` | 最小 FastAPI 服务 | HTTP 路由、请求响应 |
| `sync_vs_async.py` | 同步 vs 异步对比 | `async/await`、并发 |
| `sql_demo.py` | SQLite 增删查改 | 关系型数据库基础 |
| `chat_demo.py` | 多轮对话 | messages 列表、上下文重发 |
| `stream_demo.py` | 流式输出 | `stream=True`、增量打印 |
| `function_demo.py` | Function Calling | tools 说明书、tool_calls 解析 |
| `react_agent.py` | **手搓 ReAct Agent** | 主循环、工具路由、多轮调用 |
| `embed_demo.py` | 文本向量化 | embedding、余弦相似度 |
| `chroma_demo.py` | 向量数据库入门 | Chroma 入库与查询 |
| `rag_demo.py` | **RAG 问答系统** | 检索 → 增强 → 生成、防幻觉 |

## 技术栈

- **语言**：Python 3.11
- **LLM**：DeepSeek API（OpenAI 兼容协议）
- **向量化**：fastembed + `BAAI/bge-small-zh-v1.5`（中文，本地运行）
- **向量库**：ChromaDB（本地持久化）
- **Web**：FastAPI

## 怎么跑

### 1. 准备环境

```bash
git clone https://github.com/QRT5010/agent-bootcamp.git
cd agent-bootcamp

python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash
# Linux / macOS 用: source .venv/bin/activate

pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 DeepSeek API Key：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

> 申请地址：https://platform.deepseek.com

### 3. 跑 RAG 问答系统

```bash
# 首次运行需要下载 embedding 模型（约 100MB），用国内镜像加速
HF_ENDPOINT=https://hf-mirror.com python rag_demo.py
```

启动后直接输入问题即可，输入 `exit` 退出：

```
你问：图书馆几点开门？

[检索命中 3 条]
答：图书馆每天早上八点开门。

你问：食堂的招牌菜是什么？

[检索命中 3 条]
答：资料里没有相关规定。
```

**最后一条是重点**：问到知识库里**没有**的内容时，系统会明确回答"没有相关规定"，而不是编造答案。

## RAG 是怎么工作的

```
用户提问
   ↓
① 把问题转成向量（embedding）
   ↓
② 去向量库找最相似的 3 条资料（检索）
   ↓
③ 把资料 + 问题拼成提示词（增强）
   ↓
④ 交给 LLM，要求"只根据资料回答"（生成）
   ↓
答案
```

第 ④ 步的提示词里写死了"**如果资料里找不到答案，就回答'资料里没有相关规定'**"，这是防止模型胡编（幻觉）的关键。

## 项目结构

```
agent-bootcamp/
├── main.py              # FastAPI 最小服务
├── sync_vs_async.py     # 同步/异步对比
├── sql_demo.py          # SQLite 示例
├── chat_demo.py         # 多轮对话
├── stream_demo.py       # 流式输出
├── function_demo.py     # Function Calling
├── react_agent.py       # 手搓 ReAct Agent
├── embed_demo.py        # 向量化 + 相似度
├── chroma_demo.py       # Chroma 向量库
├── rag_demo.py          # RAG 问答系统
└── requirements.txt     # 依赖清单
```

## 学习路线

本仓库按 8 天计划推进，每天一层：

| 天 | 主题 |
|---|---|
| D1 | 环境 / Git / FastAPI 入门 |
| D2 | FastAPI 进阶 / 异步 / SQL |
| D3 | LLM API / 流式 / Function Calling / ReAct Agent |
| D4 | 向量化 / 向量库 / RAG |
| D5+ | 交通规范 Agent / 部署 / 更多 |

## License

MIT

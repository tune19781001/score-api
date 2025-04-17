from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
import os

# 永続保存フォルダを指定（Render対応）
persist_dir = "./memory_store"
os.makedirs(persist_dir, exist_ok=True)

# ベクトル記憶の初期化（今度はファイル保存あり！）
embedding = OpenAIEmbeddings()
vectorstore = Chroma(
    embedding_function=embedding,
    persist_directory=persist_dir
)

# LangChain用の記憶メモリを作成
memory = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

def save_judgment(input_text: str, result: str):
    """恒川さんの判断を記録する関数"""
    memory.save_context({"input": input_text}, {"output": result})
    vectorstore.persist()  # 🧠 保存処理を追加！
    print("✅ 記録完了（ファイル保存済み）")

def search_similar(input_text: str):
    """似た判断を検索する関数"""
    results = memory.load_memory_variables({"input": input_text})
    return results

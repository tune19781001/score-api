from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory

# ベクトル記憶の初期化（Render対応：保存せずにメモリ上で動作）
embedding = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embedding)  # in_memoryは不要になった

# LangChain用の記憶メモリを作成
memory = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

def save_judgment(input_text: str, result: str):
    """恒川さんの判断を記録する関数"""
    memory.save_context({"input": input_text}, {"output": result})
    print("✅ 記録完了！")

def search_similar(input_text: str):
    """似た判断を検索する関数"""
    results = memory.load_memory_variables({"input": input_text})
    return results

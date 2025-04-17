from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory

# ベクトル記憶の初期化
embedding = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./memory_store", embedding_function=embedding)

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

# memory_bot.py

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory

# ✅ ベクトル記憶（判断履歴）用
embedding = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embedding, persist_directory="./memory_store")
memory_retriever = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

# ✅ 会話メモリ（チャット文脈）用
conversation_memory = ConversationBufferMemory(return_messages=True)

# ✅ 記録（判断履歴）
def save_judgment(input_text: str, result: str):
    memory_retriever.save_context({"input": input_text}, {"output": result})
    print("✅ 判断を記録しました")

# ✅ 検索（似た判断履歴）
def search_similar(input_text: str):
    results = memory_retriever.load_memory_variables({"input": input_text})
    return results

# ✅ 会話履歴に追加（チャット文脈）
def update_conversation(user_input: str, bot_output: str):
    conversation_memory.save_context({"input": user_input}, {"output": bot_output})

# ✅ 会話履歴の取得
def get_conversation_history():
    return conversation_memory.buffer

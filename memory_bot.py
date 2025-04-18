from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains.conversation.memory import ConversationBufferMemory
from pinecone import Pinecone, ServerlessSpec  # ← 新しい方法でimport
import os

# ✅ Pinecone接続情報
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "pcsk_2Wt6v2_Rcics4ScEmeWne23uk1PF3VzyZA7EXKAgyMiGNdgVhDdJHCtsPp2LheYYVTSp78")
INDEX_NAME = "judgment-log"

# ✅ Pinecone初期化（新SDK対応）
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# ✅ Embeddings（OpenAI）
embedding = OpenAIEmbeddings()

# ✅ LangChain用ベクトルストア
vectorstore = LangchainPinecone(
    index=index,
    embedding=embedding,
    text_key="text"
)

# ✅ 判断記憶用メモリ
memory_retriever = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

# ✅ 会話メモリ
conversation_memory = ConversationBufferMemory(return_messages=True)

def save_judgment(input_text: str, result: str):
    memory_retriever.save_context({"input": input_text}, {"output": result})
    print("✅ Pineconeに判断を記録しました")

def search_similar(input_text: str):
    results = memory_retriever.load_memory_variables({"input": input_text})
    return results

def update_conversation(user_input: str, bot_output: str):
    conversation_memory.save_context({"input": user_input}, {"output": bot_output})

def get_conversation_history(limit=3):
    messages = conversation_memory.chat_memory.messages[-limit*2:]
    history = ""
    for i in range(0, len(messages), 2):
        user = messages[i].content
        bot = messages[i+1].content if i+1 < len(messages) else ""
        history += f"input: {user}\noutput: {bot}\n"
    return history

def get_response(user_input: str):
    conversation_memory.chat_memory.add_user_message(user_input)
    response = f"あなたの言ったこと: {user_input}"
    conversation_memory.chat_memory.add_ai_message(response)
    return response

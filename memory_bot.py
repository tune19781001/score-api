
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone as LangchainPinecone  # ← ← ← ここ変更！
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains.conversation.memory import ConversationBufferMemory
from pinecone import Pinecone, ServerlessSpec
import os

# ✅ 環境変数からAPIキー取得
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "あなたのキー")
INDEX_NAME = "judgment-log"

# ✅ Pinecone新SDK対応（インスタンス作成）
pc = Pinecone(api_key=PINECONE_API_KEY)

# ✅ インデックスを取得（※ここは旧形式と同じ）
index = pc.Index(INDEX_NAME)

# ✅ OpenAI Embedding モデル
embedding = OpenAIEmbeddings()

# ✅ LangChain対応のPineconeラッパー
vectorstore = LangchainPinecone(
    index=index,
    embedding=embedding,
    text_key="text"  # メタデータではなく本文を保存・検索
)

# ✅ 検索メモリの準備
memory_retriever = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

# ✅ 会話メモリ（チャットの流れ保持）
conversation_memory = ConversationBufferMemory(return_messages=True)

# ✅ 判断ログの保存
def save_judgment(input_text: str, result: str):
    memory_retriever.save_context({"input": input_text}, {"output": result})
    print("✅ Pineconeに判断を記録しました")

# ✅ 類似判断の検索
def search_similar(input_text: str):
    return memory_retriever.load_memory_variables({"input": input_text})

# ✅ 会話記録
def update_conversation(user_input: str, bot_output: str):
    conversation_memory.save_context({"input": user_input}, {"output": bot_output})

# ✅ 会話履歴の取得（直近n件）
def get_conversation_history(limit=3):
    messages = conversation_memory.chat_memory.messages[-limit*2:]
    history = ""
    for i in range(0, len(messages), 2):
        user = messages[i].content
        bot = messages[i+1].content if i+1 < len(messages) else ""
        history += f"input: {user}\noutput: {bot}\n"
    return history

# ✅ 応答生成（仮のエコー応答）
def get_response(user_input: str):
    conversation_memory.chat_memory.add_user_message(user_input)
    response = f"あなたの言ったこと: {user_input}"
    conversation_memory.chat_memory.add_ai_message(response)
    return response

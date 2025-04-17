# memory_bot.py（Pinecone版 + 会話補助あり）

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains.conversation.memory import ConversationBufferMemory
import pinecone

# ✅ Pinecone接続情報（恒川さんの値に書き換えてね！）
PINECONE_API_KEY = "pcsk_2Wt6v2_Rcics4ScEmeWne23uk1PF3VzyZA7EXKAgyMiGNdgVhDdJHCtsPp2LheYYVTSp78"
PINECONE_ENV = "us-east-1"  # ← Environment名
INDEX_NAME = "judgment-log"

# ✅ 初期化（最初に1回だけ必要）
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)

# ✅ Embeddings（OpenAI埋め込みモデル）
embedding = OpenAIEmbeddings()

# ✅ Pineconeベースのベクトルストア
vectorstore = Pinecone.from_existing_index(
    index_name=INDEX_NAME,
    embedding=embedding
)

# ✅ 判断記憶用メモリ
memory_retriever = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

# ✅ 会話メモリ（チャット文脈用）
conversation_memory = ConversationBufferMemory(return_messages=True)

# ✅ 記録（判断ログ）
def save_judgment(input_text: str, result: str):
    memory_retriever.save_context({"input": input_text}, {"output": result})
    print("✅ Pineconeに判断を記録しました")

# ✅ 類似検索（判断の再利用）
def search_similar(input_text: str):
    results = memory_retriever.load_memory_variables({"input": input_text})
    return results

# ✅ 会話メモリに追加（チャット文脈の保持）
def update_conversation(user_input: str, bot_output: str):
    conversation_memory.save_context({"input": user_input}, {"output": bot_output})

# ✅ 会話履歴の取得（最新のみ）
def get_conversation_history(limit=3):
    messages = conversation_memory.chat_memory.messages[-limit*2:]  # 入出力ペア
    history = ""
    for i in range(0, len(messages), 2):
        user = messages[i].content
        bot = messages[i+1].content if i+1 < len(messages) else ""
        history += f"input: {user}\noutput: {bot}\n"
    return history

# ✅ GPTが返答を生成するときに使う関数（文脈考慮）
def get_response(user_input: str):
    conversation_memory.chat_memory.add_user_message(user_input)
    response = f"あなたの言ったこと: {user_input}"
    conversation_memory.chat_memory.add_ai_message(response)
    return response
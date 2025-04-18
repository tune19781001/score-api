# memory_bot.py（Pinecone新SDK対応 + 会話補助あり + 最新LangChain準拠）

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains.conversation.memory import ConversationBufferMemory
import os

# ✅ Pinecone接続情報
# APIキーと使用するインデックス名を環境変数 or 直接指定でセット
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "pcsk_2Wt6v2_Rcics4ScEmeWne23uk1PF3VzyZA7EXKAgyMiGNdgVhDdJHCtsPp2LheYYVTSp78")
INDEX_NAME = "judgment-log"

# ✅ Embeddings（OpenAI）
# テキストをベクトル化するためのOpenAI埋め込みモデル
embedding = OpenAIEmbeddings()

# ✅ LangChain用ベクトルストア（最新版）
# LangChainが使う検索用インターフェースとしてPineconeをラップ
vectorstore = LangchainPinecone(
    index_name=INDEX_NAME,
    embedding=embedding,
    pinecone_api_key=PINECONE_API_KEY
)

# ✅ 判断記憶用メモリ
# ユーザーの入力とそれに対する出力（判断）を記録・検索できるメモリ
memory_retriever = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

# ✅ 会話メモリ（チャット文脈用）
# 直前の会話の流れを保持するための履歴メモリ（最大で数件）
conversation_memory = ConversationBufferMemory(return_messages=True)

# ✅ 記録（判断ログ）
# 入力と判断結果をPineconeに保存する関数
def save_judgment(input_text: str, result: str):
    memory_retriever.save_context({"input": input_text}, {"output": result})
    print("✅ Pineconeに判断を記録しました")

# ✅ 類似検索（判断の再利用）
# 入力に似た過去の判断履歴をPineconeから検索する
def search_similar(input_text: str):
    results = memory_retriever.load_memory_variables({"input": input_text})
    return results

# ✅ 会話メモリに追加（チャット文脈の保持）
# 会話の中でやりとりされた内容を履歴として保存
# 例："じゃあ保存して" に対応するために、直前の内容を記録
def update_conversation(user_input: str, bot_output: str):
    conversation_memory.save_context({"input": user_input}, {"output": bot_output})

# ✅ 会話履歴の取得（最新のみ）
# 直近のやりとりを数件（デフォルトは3セット）取得
# GPTなどが「直前の流れ」を理解するために使える
def get_conversation_history(limit=3):
    messages = conversation_memory.chat_memory.messages[-limit*2:]  # 入出力ペア
    history = ""
    for i in range(0, len(messages), 2):
        user = messages[i].content
        bot = messages[i+1].content if i+1 < len(messages) else ""
        history += f"input: {user}\noutput: {bot}\n"
    return history

# ✅ GPTが返答を生成するときに使う関数（文脈考慮）
# 会話における入力を受け取り、仮の応答（エコー）を返す
# 本番ではここにLLMの応答処理を組み込む想定
# 会話履歴としても記録される

def get_response(user_input: str):
    conversation_memory.chat_memory.add_user_message(user_input)
    response = f"あなたの言ったこと: {user_input}"
    conversation_memory.chat_memory.add_ai_message(response)
    return response
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone as LangchainPinecone
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains.conversation.memory import ConversationBufferMemory
from pinecone import Pinecone, ServerlessSpec
import os

# Get API key from environment variable
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "your-key")
INDEX_NAME = "judgment-log"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Get index
index = pc.Index(INDEX_NAME)

# OpenAI Embedding model
embedding = OpenAIEmbeddings()

# Pinecone wrapper for LangChain
vectorstore = LangchainPinecone(
    index=index,
    embedding=embedding,
    text_key="text"
)

# Prepare retriever memory
memory_retriever = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())

# Conversation memory for tracking chat history
conversation_memory = ConversationBufferMemory(return_messages=True)

# Save judgment result to Pinecone
def save_judgment(input_text: str, result: str):
    memory_retriever.save_context({"input": input_text}, {"output": result})
    print("Saved judgment to Pinecone.")

# Search similar judgment history
def search_similar(input_text: str):
    return memory_retriever.load_memory_variables({"input": input_text})

# Update chat history
def update_conversation(user_input: str, bot_output: str):
    conversation_memory.save_context({"input": user_input}, {"output": bot_output})

# Get recent conversation history (last n pairs)
def get_conversation_history(limit=3):
    messages = conversation_memory.chat_memory.messages[-limit*2:]
    history = ""
    for i in range(0, len(messages), 2):
        user = messages[i].content
        bot = messages[i+1].content if i+1 < len(messages) else ""
        history += f"input: {user}\noutput: {bot}\n"
    return history

# Generate response (basic echo bot)
def get_response(user_input: str):
    conversation_memory.chat_memory.add_user_message(user_input)
    response = f"You said: {user_input}"
    conversation_memory.chat_memory.add_ai_message(response)
    return response

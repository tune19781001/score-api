{\rtf1\ansi\ansicpg932\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from langchain.vectorstores import Chroma\
from langchain.embeddings import OpenAIEmbeddings\
from langchain.memory import VectorStoreRetrieverMemory\
\
# \uc0\u12505 \u12463 \u12488 \u12523 \u35352 \u25014 \u12398 \u21021 \u26399 \u21270 \
embedding = OpenAIEmbeddings()\
vectorstore = Chroma(persist_directory="./memory_store", embedding_function=embedding)\
\
# LangChain\uc0\u29992 \u12398 \u35352 \u25014 \u12513 \u12514 \u12522 \u12434 \u20316 \u25104 \
memory = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())\
\
def save_judgment(input_text: str, result: str):\
    """\uc0\u24658 \u24029 \u12373 \u12435 \u12398 \u21028 \u26029 \u12434 \u35352 \u37682 \u12377 \u12427 \u38306 \u25968 """\
    memory.save_context(\{"input": input_text\}, \{"output": result\})\
    print("\uc0\u9989  \u35352 \u37682 \u23436 \u20102 \u65281 ")\
\
def search_similar(input_text: str):\
    """\uc0\u20284 \u12383 \u21028 \u26029 \u12434 \u26908 \u32034 \u12377 \u12427 \u38306 \u25968 """\
    results = memory.load_memory_variables(\{"input": input_text\})\
    return results\
}
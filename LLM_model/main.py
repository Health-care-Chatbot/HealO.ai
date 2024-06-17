# from server import initServer

from LLM_controllers import *
from model_server import create_app
from Templates import template_prompt, prompt_examples
from load_data import load_data, convert_to_documents
from vectordb import is_vectordb_empty, empty_vectordb
from model import HealOLLM

from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.llms import Replicate
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma

from typing import List
import replicate
from dotenv import load_dotenv
import json
import sys


def initServer():
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
    return app

def initLLM():    
    load_dotenv()
    # sys.stdin = open('testfile.txt', 'r')
    llm = HealOLLM()
    # llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest', temperature=0.9)
  
    set_llm(llm)
    embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")
    vector_db = Chroma(embedding_function=embedder, persist_directory='database/tool_mistake_db', relevance_score_fn='similarity_search_with_score', )

    question_answer_dataframe = load_data("data/iCliniq.json")
    question_answer_documents = convert_to_documents(question_answer_dataframe)
    
    if is_vectordb_empty(vector_db):
        vector_db.add_documents(question_answer_documents)
    set_vector_db(vector_db)    


if __name__ == '__main__':
    initLLM()
    initServer()
    
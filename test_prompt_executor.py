from Templates import template_prompt, prompt_examples
from load_data import load_data, convert_to_documents
from vectordb import is_vectordb_empty, empty_vectordb

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
sys.stdin = open('testfile.txt', 'r')

llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest', temperature=0.9)
# llm = Replicate(model="replicate/llama70b-v2-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48", model_kwargs={"temperature":0.1, "max_length":500})

def get_chat_prompt(examples):
    chat_prompt = template_prompt.get_chat_prompt(examples)
    return chat_prompt

def extract_from_bullets(string: str) -> List[str]:
    """
    Extracts sentences from a string that starts with a number followed by a period like 1., 2., 3., etc.
    
    Args:
        string (str): The input string containing bullet points.
        
    Returns:
        list: A list of sentences extracted from the bullet points.
    """
    lines = string.strip().split("\n")
    sentences = []
    counter = 1
    for line in lines:
        if line.startswith(str(counter)):
            sentences.append(line[line.find(".")+1:])
            counter += 1
    return [sentence for sentence in sentences if len(sentence)>0]

def get_refined_prompt(examples):
    refined_prompt = template_prompt.get_refined_prompt2(examples)
    return refined_prompt

def get_product_prompt(examples):
    product_prompt = template_prompt.get_product_prompt(examples)
    return product_prompt


if __name__ == "__main__":
    load_dotenv()

    embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = Chroma(embedding_function=embedder, persist_directory='database/tool_mistake_db',  relevance_score_fn='similarity_search_with_score')

    question_answer_dataframe = load_data("data/iCliniq.json")
    question_answer_documents = convert_to_documents(question_answer_dataframe)
    
    if is_vectordb_empty(vector_db):
        vector_db.add_documents(question_answer_documents)
    
    random_examples = json.load(open("data/initial_fewshots.json", "r"))
    random_examples = prompt_examples.get_chat_example_prompt1(random_examples)
    chat_prompt = get_chat_prompt(random_examples)

    first_chain = LLMChain(llm=llm, prompt=chat_prompt)

    background = input("What is your background?: ")
    symptoms = input("Symptoms: ")
    query = f"This is my background : {background} and these are my symptoms: {symptoms}"

    chat_input = {
        "name": "HealO",
        "query": query, 
    }
    
    response = first_chain.invoke(chat_input)

    extracted_lines = extract_from_bullets(response["text"])
    documents_list = [vector_db.similarity_search(line, k=2) for line in extracted_lines]
    examples_list = [document.metadata for documents in documents_list for document in documents]

    refined_prompt = prompt_examples.get_refined_example_prompt1(examples_list)
    refined_prompt = get_refined_prompt(refined_prompt)

    print("##########\n#######")

    memory = ConversationBufferMemory(memory_key="chat_history", input_key="query", return_messages=True)
    second_chain = LLMChain(llm=llm, prompt=refined_prompt, memory=memory)

    chat_input = {
        "name": "HealO",
        "query": f"This is my background : {background} and these are my symptoms: {symptoms}", 
    }

    response = second_chain.invoke(chat_input)
    while True:
        print(response["text"])
        question = input("User: ")

        if question.strip()=="exit":
            exit()
        
        chat_input = {
            "name": "HealO",
            "query": query, 
        }
        response = second_chain.invoke(chat_input)


    # random_examples3 = prompt_examples.get_product_example_prompt1(random_examples)
    # product_prompt = get_product_prompt(random_examples3)
    # Uncomment below line to test prompt on gemini-llm

    # print(product_prompt.format_messages(name="HealO", background="I am a 20 year old"))
    # test_prompt_on_llm(chat_prompt)
    # test_prompt_on_llm(refined_prompt)
    # test_prompt_on_llm(product_prompt)



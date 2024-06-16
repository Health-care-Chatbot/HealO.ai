# LLM_controllers.py -> This file is controller for llm model to manage between api calls and llm chains.

from Templates import template_prompt, prompt_examples
from typing import List
import pickle
# from model_server import prompt_handler
import json
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
# from main import get_vector_db, get_llm

chain_storage = {}

vector_db = None
llm = None
background = ""


def get_background_form():
    global background
    return background

def set_background_form(background_form):
    global background
    background = background_form
    
def get_vector_db():
    global vector_db
    return vector_db

def set_vector_db(vector):
    global vector_db
    vector_db = vector

def get_llm():
    global llm
    return llm

def set_llm(llm_instance):
    global llm
    llm = llm_instance

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

def serialize_chain(chain):
    """Serialize the LLMChain object to a string."""
    return pickle.dumps(chain)

def deserialize_chain(serialized_chain):
    """Deserialize the string back to an LLMChain object."""
    return pickle.loads(serialized_chain)

def store_chain(user_id, chain):
    """Store the serialized chain in the global dictionary."""
    global chain_storage
    chain_storage[user_id] = chain 

def get_chain(user_id):
    """Retrieve and deserialize the chain from the global dictionary."""
    global chain_storage
    serialized_chain = chain_storage.get(user_id)
    if serialized_chain:
        return serialized_chain
    return None

def get_refined_chain(user_id, chat_input, background):
    llm = get_llm()
    
    """Get the refined chain for the user."""
    random_examples = json.load(open("data/initial_fewshots.json", "r"))
    random_examples = prompt_examples.get_chat_example_prompt1(random_examples)
    chat_prompt = get_chat_prompt(random_examples)

    first_chain = LLMChain(llm=llm, prompt=chat_prompt)
    query = f"This is my background : {background} and these are my symptoms: {chat_input}"
    chat_input = {
        "name": "HealO",
        "query": query, 
    }
    response = first_chain.invoke(chat_input)
    vector_db = get_vector_db()
    extracted_lines = extract_from_bullets(response["text"])
    documents_list = [vector_db.similarity_search(line, k=2) for line in extracted_lines]
    examples_list = [document.metadata for documents in documents_list for document in documents]

    refined_prompt = prompt_examples.get_refined_example_prompt1(examples_list)
    refined_prompt = get_refined_prompt(refined_prompt)

    print("##########\n#######")      
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="query", return_messages=True)
    second_chain = LLMChain(llm=llm, prompt=refined_prompt, memory=memory)

    # chat_input = {
    #     "name": "HealO",
    #     "query": f"This is my background : {background} and these are my symptoms: {chat_input}", 
    # }
  
    store_chain(user_id, second_chain)
    # response = second_chain.invoke(chat_input) 
    return second_chain
       

def get_llm_response(user_id, chat_input, background):
    """Get the response from the LLMChain object."""
    
    chain = get_chain(user_id)
    if(chain == None):
        print("Refined Chain not found. Creating a new one")
        chain = get_refined_chain(user_id, chat_input, background)
    print("refined chain found")
    query = f"This is my background : {background} and these are my symptoms: {chat_input}"
    chat_input = {
        "name": "HealO",
        "query": query, 
    }
    response = chain.invoke(chat_input)
    return response["text"]
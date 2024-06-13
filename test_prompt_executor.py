from Templates import template_prompt, prompt_examples
from load_data import load_data, convert_to_documents
from vectordb import is_vectordb_empty, empty_vectordb

from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.llms import Replicate
from langchain.memory import ConversationBufferMemory

from langchain.vectorstores.chroma import Chroma

from dotenv import load_dotenv

example_query = """I have a runny nose and a cough and my head hurts a lot"""

example_response = """
1. Common Cold: This is the most likely culprit, especially during certain seasons. A runny nose, cough, and headache are hallmark symptoms.

2. Sinusitis:  A cold can sometimes lead to a sinus infection, causing facial pain and pressure in addition to the cold symptoms.

3. Influenza (Flu):  The flu often comes with more intense symptoms than a cold, including fever, body aches, and fatigue, along with your listed symptoms. 

4. Allergic Rhinitis: If your symptoms are persistent or worsen at certain times of the year, allergies could be the cause.

5. COVID-19: While less likely if your symptoms are mild, it's still possible. COVID-19 can cause a wide range of symptoms, including those you're experiencing.
"""
def get_chat_prompt(examples):
    chat_prompt = template_prompt.get_chat_prompt(examples)
    # chat_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptoms="I have a runny nose and a cough")
    # print(chat_prompt)
    return chat_prompt

def extract_from_bullets(string):
    lines = string.strip().split("\n")
    sentences = []
    counter = 1
    for line in lines:
        if line.startswith(str(counter)):
            sentences.append(line[line.find(".")+1:])
            counter += 1
    return [sentence for sentence in sentences if len(sentence)>0]

def get_refined_prompt(examples):
    #Hardcoded prompt for refined example for now
    refined_prompt = template_prompt.get_refined_prompt2(examples)
    # refined_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptoms="I have a runny nose and a cough")
    # print(refined_prompt)
    return refined_prompt

def get_product_prompt(examples):
    product_prompt = template_prompt.get_refined_prompt2(examples)
    return product_prompt

# Test prompts on gemini-llm model 
def test_prompt_on_llm(prompt) :
    llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest', temperature=0.1, memory=ConversationBufferMemory, ai_prefix="Doctor", human_prefix="Patient")
    # llm = Replicate(model="replicate/llama70b-v2-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48", model_kwargs={"temperature":0.1, "max_length":500})

    chat_chain = LLMChain(llm=llm, prompt=prompt)
    chat_input = {
        "name": "HealO",
        "background":"I am a 8 year old male", 
        "symptoms":"My throat hurts and it feels swollen at the back"
    }
    # response = chat_chain.run(chat_input)
    prediction_msg = chat_chain.run(chat_input)
    return prediction_msg


if __name__ == "__main__":
    load_dotenv()

    embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = Chroma(embedding_function=embedder, persist_directory='database/tool_mistake_db',  relevance_score_fn='similarity_search_with_score')

    question_answer_dataframe = load_data()
    question_answer_documents = convert_to_documents(question_answer_dataframe)
    
    if is_vectordb_empty(vector_db):
        vector_db.add_documents(question_answer_documents)
    
    # random_examples = [{"input":question_answer_dataframe.iloc[i].input, "output":question_answer_dataframe.iloc[i].output} for i in range(5)]
    random_examples = [{"input":example_query, "output":example_response}]

    random_examples = prompt_examples.get_chat_example_prompt1(random_examples)

    # print(random_examples)
    # print(random_examples2)
    #TODO: @ShreeSinghi change the hardcoded prompt to auto-generated refined example prompt
    chat_prompt = get_chat_prompt(random_examples)
    response = test_prompt_on_llm(chat_prompt)
    extracted_lines = extract_from_bullets(response)

    documents_list = [vector_db.similarity_search(line, k=2, search_type='similarity') for line in extracted_lines]
    examples_list = [document.metadata for documents in documents_list for document in documents]

    random_examples2 = prompt_examples.get_refined_example_prompt1(examples_list)
    refined_prompt = get_refined_prompt(random_examples2)
    print("##########\n#######")
    print(test_prompt_on_llm(refined_prompt))

    # random_examples3 = prompt_examples.get_product_example_prompt1(random_examples)
    # product_prompt = get_product_prompt(random_examples3)
    # Uncomment below line to test prompt on gemini-llm

    # print(product_prompt.format_messages(name="HealO", background="I am a 20 year old"))

    # 
    # 
    # test_prompt_on_llm(product_prompt)



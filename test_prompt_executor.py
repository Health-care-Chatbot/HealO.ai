from Templates import template_prompt, prompt_examples
# from load_data import load_data, convert_to_documents
# from vectordb import is_vectordb_empty, empty_vectordb
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langchain.vectorstores.chroma import Chroma

from dotenv import load_dotenv

def get_chat_prompt(examples):
    chat_prompt = template_prompt.get_chat_prompt(examples)
    # chat_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptoms="I have a runny nose and a cough")
    # print(chat_prompt)
    return chat_prompt

def get_refined_prompt(examples):
        #Hardcoded prompt for refined example for now
    refined_prompt = template_prompt.get_refined_prompt2(examples)
    # refined_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptoms="I have a runny nose and a cough")
    # print(refined_prompt)
    return refined_prompt

# Test prompts on gemini-llm model 
def test_prompt_on_llm(prompt) :
    llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest', temperature=0.9)
    # response = llm.invoke("How are you")
    chat_chain = LLMChain(llm=llm, prompt=prompt)
    # response = llm.invoke(prompt)
    chat_input = {
        "name": "HealO",
        "background":"I am a 20 year old male", 
        "symptoms":"I have a runny nose and a cough"
    }
    # response = chat_chain.run(chat_input)
    prediction_msg = chat_chain.run(chat_input)
    print(prediction_msg)


if __name__ == "__main__":
    load_dotenv()

    # embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # vector_db = Chroma(embedding_function=embedder, persist_directory= 'database/tool_mistake_db',  relevance_score_fn='similarity_search_with_score')

    # question_answer_dataframe = load_data()
    # question_answer_strings = convert_to_documents(question_answer_dataframe)
    
    # empty_vectordb(vector_db)
    # if is_vectordb_empty(vector_db):
    #     vector_db.add_documents(question_answer_strings)
    #     print(len(question_answer_strings), vector_db.get()["ids"])
    
    # random_examples = [{"input":question_answer_dataframe.iloc[i].input, "output":question_answer_dataframe.iloc[i].output} for i in range(5)]
    
    random_examples = prompt_examples.get_chat_example_prompt1()
    random_examples2 = prompt_examples.get_refined_example_prompt1()
    # print(random_examples)
    # print(random_examples2)
    #TODO: @ShreeSinghi change the hardcoded prompt to auto-generated refined example prompt
    chat_prompt = get_chat_prompt(random_examples)
    refined_prompt = get_refined_prompt(random_examples2)
    # Uncomment below line to test prompt on gemini-llm
    # print(refined_prompt)
    test_prompt_on_llm(chat_prompt)



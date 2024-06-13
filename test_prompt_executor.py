from Templates import template_prompt, prompt_examples
from load_data import load_data, convert_to_documents

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores.chroma import Chroma

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    chat_prompt = template_prompt.get_chat_prompt()
    chat_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptoms="I have a runny nose and a cough")
    print(chat_prompt)

    #TODO: @ShreeSinghi change the hardcoded prompt to auto-generated refined example prompt

    embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = Chroma(embedding_function=embedder, persist_directory= 'database/tool_mistake_db',  relevance_score_fn='similarity_search_with_score')
    
    question_answer_dataframe = load_data()
    question_answer_strings = convert_to_documents(question_answer_dataframe)
    vector_db.add_documents(question_answer_strings)

    #Hardcoded prompt for refined example for now
    refined_prompt = template_prompt.get_refined_prompt2(prompt_examples.get_refined_example_prompt1())
    refined_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptoms="I have a runny nose and a cough")
    print(refined_prompt)

# get_refined_prompt2



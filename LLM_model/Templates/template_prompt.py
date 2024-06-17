from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain_core.prompts.prompt import (PromptTemplate)
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)
from Templates import prompt_examples

# Prompt template for first llm processing.

# System message prompt to manupulate the LLM model for accuracy
base_sys_prompt1: PromptTemplate = PromptTemplate(
    input_variables=["name"],
    template="""You are a helpful Health AI bot and I can't consult doctor because of unavailability. It is your duty to help . You need to provide user with sensitive informations,. Your name is {name}.
                Use the following pieces of information to answer the user's question.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                Only return the helpful answer below and nothing else and never ask to consult doctor. """
)
#____________________________________________________________________________________________________________

def get_chat_prompt(example_prompt) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=base_sys_prompt1),
            example_prompt,
            AIMessagePromptTemplate.from_template("Please provide me with patients background and symptoms."),
            HumanMessagePromptTemplate.from_template("{query}. Can you please list out 5 most likely possible conditions I might have?"),      
        ]
    )
#============================================================================================================

# Prompt template for second llm processing.

#Sys messesage prompt to manipulate the LLM model for refining
base_sys_prompt2: PromptTemplate = PromptTemplate(
    input_variables=["name"],
    template="""You are a honest helpful doctor as well as a document scraper. You need to provide user with sensitive informations, so be specific with details. Your name is {name}.
                Use the following pieces of information to answer the user's question.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                Look for the most relevant information in the examples above, if not found use your knowledge but Only return the helpful answer below and nothing else.
                If you want more information from the patient please ask for additional information"""
)
#____________________________________________________________________________________________________________

def get_refined_prompt2(get_refined_example_prompt) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=base_sys_prompt2),
            get_refined_example_prompt,
            AIMessagePromptTemplate.from_template("Please provide me with patients background and symptoms."),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{query}"),      
        ]
    )
#============================================================================================================

# Prompt template for product items fetch

#Sys messesage prompt for configuring llm to extract products from the response of refined llm
base_sys_prompt3: PromptTemplate = PromptTemplate(
    input_variables=["name"],
    template="""You are a honest helpful Health AI bot as well as a product/medicine name extractor. You need to provide user with sensitive informations, so be specific with details. Your name is {name}.
                Take the next prompt which is an prescription to a patient 
                and extract any product names Only Product/drug name and not frequency and other details mentioned as a cure of disease in the response.
                Information is sensitive and health-related so dont make up with the answer.
                Just answer whatever you find in text to be the  product or medicine name needed for cure.
                Below is a sample example of the ques and answer. Follow this pattern to extract the product name.
                Return nothing if the prompt does not have any product name.
                Also, Important to note to output response as array/list of names of products only and not quantity, refer to examples for format of output and stick to it."""
)
#____________________________________________________________________________________________________________

def get_product_prompt(get_product_example_prompt) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=base_sys_prompt3),
            get_product_example_prompt,
            AIMessagePromptTemplate.from_template("Please provide me with the prompt to extract items to buy."),
            HumanMessagePromptTemplate.from_template("This is my prescription : {prescription}. Make sure to output as array of product names only."),      
        ]
    )


# if __name__ == "__main__":
#     chat_prompt = get_chat_prompt()
#     chat_prompt.format_messages(name="HealO", user_input="What is the best way to treat a cold?")









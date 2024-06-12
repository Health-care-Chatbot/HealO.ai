from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain_core.prompts.prompt import (PromptTemplate)
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
import prompt_examples


# Prompt template for first llm processing.

# System message prompt to manupulate the LLM model for accuracy
base_sys_prompt1: PromptTemplate = PromptTemplate(
    input_variables=["name"],
    template="""You are a good helpful Health AI bot. You need to provide user with sensitive informations,. Your name is {name}."""
)

conditional_sys_prompt1 = PromptTemplate.from_template("""Use the following pieces of information to answer the user's question.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                Only return the helpful answer below and nothing else.
                """),
#____________________________________________________________________________________________________________

def get_chat_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=base_sys_prompt1),
            HumanMessagePromptTemplate.from_template("Hello, how are you doing?"),
            AIMessagePromptTemplate.from_template("I'm doing well, thanks! "),
            SystemMessagePromptTemplate(prompt=conditional_sys_prompt1),
            prompt_examples.get_chat_example_prompt1(),
            AIMessagePromptTemplate.from_template("Please provide me with patients background and senarios."),
            HumanMessagePromptTemplate.from_template("{user_input}"),
            
        ]
    )

#____________________________________________________________________________________________________________

# Prompt template for second llm processing.

#Sys messesage prompt to manipulate the LLM model for refining
base_sys_prompt2: PromptTemplate = PromptTemplate(
    input_variables=["name"],
    template="""You are a good helpful Health AI bot. You need to provide user with sensitive informations,. Your name is {name}."""
)


#____________________________________________________________________________________________________________
# if __name__ == "__main__":
#     chat_prompt = get_chat_prompt()
#     chat_prompt.format_messages(name="HealO", user_input="What is the best way to treat a cold?")
#     print(chat_prompt)








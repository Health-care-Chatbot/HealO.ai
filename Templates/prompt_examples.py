from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

# These examples are for chat-LLM to understand user pattend for questioning and answering
def get_chat_example_prompt1(examples):
    example_prompt = ChatPromptTemplate.from_messages(
        [   
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )

    few_shot_example_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    return few_shot_example_prompt

# These examples are for refiner-LLM to use the auto generated examples to find the most relevant information
def get_refined_example_prompt1(examples):
    example_prompt = ChatPromptTemplate.from_messages(
        [   
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )

    few_shot_example_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    return few_shot_example_prompt

def get_product_example_prompt1(examples):
    example_prompt = ChatPromptTemplate.from_messages(
        [   
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )

    few_shot_example_prompt = FewShotChatMessagePromptTemplate(
        examples=examples,
        input_variables=["role", "content"]
    )
    return few_shot_example_prompt


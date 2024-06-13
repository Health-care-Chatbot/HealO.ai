from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+3", "output": "5"},
    {"input": "2+3", "output": "5"},
    {"input": "2+3", "output": "5"},
    {"input": "2+3", "output": "5"},
]
# These examples are for chat-LLM to understand user pattend for questioning and answering
def get_chat_example_prompt1(examples = examples):
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
def get_refined_example_prompt1(examples = examples):
    # examples = [
    #     {"input": "2+2", "output": "4"},
    #     {"input": "2+3", "output": "5"},
    #     {"input": "2+3", "output": "5"},
    #     {"input": "2+3", "output": "5"},
    #     {"input": "2+3", "output": "5"},
    # ]

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

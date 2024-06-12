from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

def get_chat_example_prompt1():
    examples = [
        {"input": "2+2", "output": "4"},
        {"input": "2+3", "output": "5"},
        {"input": "2+3", "output": "5"},
        {"input": "2+3", "output": "5"},
        {"input": "2+3", "output": "5"},
    ]

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

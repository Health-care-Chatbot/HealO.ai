from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

examples = [
    {
        "input": "I have a persistent cough and shortness of breath.",
        "output": "These symptoms could indicate bronchitis or asthma. For bronchitis, rest, fluids, and over-the-counter cough medications may help. For asthma, an inhaler prescribed by your doctor can be effective. Please consult a healthcare provider for an accurate diagnosis and treatment plan."
    },
    {
        "input": "I have a high fever, body aches, and a severe headache.",
        "output": "These symptoms could be indicative of the flu or COVID-19. Rest, hydration, and over-the-counter fever reducers like acetaminophen or ibuprofen can help alleviate symptoms. It's important to get tested for COVID-19 and consult with a healthcare provider for the appropriate treatment."
    },
    {
        "input": "I have a burning sensation when I urinate and frequent urges to go.",
        "output": "These symptoms may suggest a urinary tract infection (UTI). Drinking plenty of water, taking cranberry supplements, and possibly an antibiotic prescribed by a doctor can help treat the infection. Please consult with a healthcare provider for an accurate diagnosis and prescription."
    },
    {
        "input": "I have a rash that is red, itchy, and spreading.",
        "output": "This could be a sign of eczema, contact dermatitis, or an allergic reaction. Applying over-the-counter hydrocortisone cream, taking antihistamines, and avoiding known allergens can help relieve the symptoms. If the rash persists, consult with a dermatologist for a precise diagnosis and treatment."
    },
    {
        "input": "I have severe chest pain that radiates to my arm and jaw.",
        "output": "These symptoms are concerning and could indicate a heart attack. Immediate medical attention is necessary. Call emergency services right away. Chewing an aspirin, if not allergic, can help while waiting for emergency responders. Quick medical intervention is crucial in such cases."
    }
]

product_prompt_examples = [
    {
    "input": "Take one capsule of Amoxicillin 500mg three times a day, one tablet of Ibuprofen 400mg every 6-8 hours as needed for pain, and one tablet of Cetirizine 10mg daily for allergy relief.",
    "output": ["Amoxicillin 500mg", "Ibuprofen 400mg", "Cetirizine 10mg"]
    },
    {
    "input": "Take two tablets of Paracetamol 500mg every 6 hours, one capsule of Omeprazole 20mg daily before breakfast, and one tablet of Loratadine 10mg once daily for allergies.",
    "output": ["Paracetamol 500mg", "Omeprazole 20mg", "Loratadine 10mg"]
    },
    {
    "input": "Administer one puff of Fluticasone Inhaler 250mcg twice daily, take one tablet of Metformin 500mg with meals, and one capsule of Doxycycline 100mg twice daily for 7 days.",
    "output": ["Fluticasone Inhaler 250mcg", "Metformin 500mg", "Doxycycline 100mg"]
    },
    {
    "input": "Take one tablet of Aspirin 81mg daily, one tablet of Lisinopril 20mg once daily, and one tablet of Atorvastatin 40mg once daily.",
    "output": ["Aspirin 81mg", "Lisinopril 20mg", "Atorvastatin 40mg"]
    },
    {
    "input": "Apply Betamethasone cream twice daily to affected area for rash.",
    "output": ["Betamethasone cream"]
    },
    {
    "input": "Take 1 tablet of Ibuprofen 200mg every 8 hours for pain relief.",
    "output": ["Ibuprofen 200mg"]
    }
]


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
        example_prompt=example_prompt,
        examples=product_prompt_examples,
        input_variables=["role", "content"]
    )
    return few_shot_example_prompt


import json
import pandas as pd
from langchain.docstore.document import Document

def load_data():
    with open('data/iCliniq.json') as f:
        data = json.load(f)
    data = pd.DataFrame.from_dict(data).drop(columns=["answer_chatdoctor", "answer_chatgpt"])

    # remove the first sentence which is always "Hello, welcome..."
    data["answer_icliniq"] = data["answer_icliniq"].apply(lambda answer: answer[answer.index(".") + 1:])

    data["input"] = data["input"].apply(lambda x: x.replace("Hello doctor,", "").replace("Hi doctor,", ""))

    data.rename(columns={"answer_icliniq": "output"}, inplace=True)
    return data.iloc[:10]

def convert_to_documents(data):
    data_point_generator = map(lambda row: f"Patient: {row['input']}\nDoctor: {row['output']}", data.to_dict(orient="records"))

    return [Document(page_content=data_point, metadata=row.copy()) for data_point, row in zip(data_point_generator, data.to_dict(orient="records"))]

if __name__ == "__main__":
    print(convert_to_documents(load_data()))
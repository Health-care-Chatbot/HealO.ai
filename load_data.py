import json
import pandas as pd
from langchain.docstore.document import Document
from typing import List

def load_data(data_path: str) -> pd.DataFrame:
    """
    Load data from a JSON file and preprocess it.

    Args:
        data_path (str): The path to the JSON file containing the data.

    Returns:
        pandas.DataFrame: The preprocessed data as a pandas DataFrame, containing columsn "input" and "output".
    """
    with open(data_path) as f:
        data = json.load(f)
    data = pd.DataFrame.from_dict(data).drop(columns=["answer_chatdoctor", "answer_chatgpt"])

    # remove the first sentence which is always "Hello, welcome..."
    data["answer_icliniq"] = data["answer_icliniq"].apply(lambda answer: answer[answer.index(".") + 1:])

    data["input"] = data["input"].apply(lambda x: x.replace("Hello doctor,", "").replace("Hi doctor,", ""))

    data.rename(columns={"answer_icliniq": "output"}, inplace=True)
    return data.iloc[:10]

def convert_to_documents(data: pd.DataFrame) -> List[Document]:
    """
    Converts the given data into a list of Document objects.

    Args:
        data (pandas.DataFrame): The input data containing 'input' and 'output' columns.

    Returns:
        list: A list of Document objects, where each Document represents a data point with the format "Patient: {input}\nDoctor: {output}".
    """
    data_point_generator = map(lambda row: f"Patient: {row['input']}\nDoctor: {row['output']}", data.to_dict(orient="records"))

    return [Document(page_content=data_point, metadata=row.copy()) for data_point, row in zip(data_point_generator, data.to_dict(orient="records"))]
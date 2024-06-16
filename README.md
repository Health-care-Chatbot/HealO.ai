# 



# HealO.ai - 
## About
The goal is to create a healthcare diagnosis chatbot that assists users by analyzing their symptoms, utilizing databases that contain real doctor-patient conversations. The solution involves leveraging task-specific datasets, Retrieval-Augmented Generation (RAG) frameworks, vector databases, and quantized LLM fine-tuning (QLoRA). The system aims to improve LLM accuracy by providing it with external accurate data, based on the user's needs and to reduce LLM hallucinations via finetuning.

![image](https://github.com/Health-care-Chatbot/HealO.ai/assets/41577064/8741fce9-60bc-4e0b-b929-4f24e3657821)

## Libraries and Frameworks Used

- [Python](https://www.python.org/): Primary language used for backend
- [LangChain](https://www.langchain.com/): To generate templates for few-shot prompting
- [PyTorch](https://pytorch.org/): Primary ML framework used
- [bitsandbytes](https://github.com/TimDettmers/bitsandbytes): For QLoRA fine-tuning

## Steps for setting up the Project

To set-up the project, follow the below commands:

* Run "python install -r requirement.txt" from LLM_model folder.
* Run "python3 main.py" from LLM_model folder to spawn the server for interacting with LLM model.
* Run "npm run" from frontend folder to start the frontend.

---
To test the backend using cli:
- Run "python install -r requirement.txt" from LLM_model folder.
- Run "python3 test_prompt_executor.py" from LLM_model folder to start the cli tool for interacting with LLM model.


import pandas as pd
import json
import os
from pprint import pprint
import bitsandbytes as bnb
import torch
import torch.nn as nn
import transformers
from datasets import load_dataset, Dataset
from huggingface_hub import notebook_login

from peft import LoraConfig, PeftConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model = "daryl149/llama-2-7b-chat-hf"
MODEL_NAME = model

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
    quantization_config=bnb_config
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
model = prepare_model_for_kbit_training(model)

import re
def get_num_layers(model):
    numbers = set()
    for name, _ in model.named_parameters():
        for number in re.findall(r'\d+', name):
            numbers.add(int(number))
    return max(numbers)

def get_last_layer_linears(model):
    names = []

    num_layers = get_num_layers(model)
    for name, module in model.named_modules():
        if str(num_layers) in name and not "encoder" in name:
            if isinstance(module, torch.nn.Linear):
                names.append(name)
    return names

config = LoraConfig(
    r=2,
    lora_alpha=32,
    target_modules=get_last_layer_linears(model),
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)

import pandas as pd

data = []
with open("test.dat", "r") as f:
    data.extend(f.readlines())
with open("train.dat", "r") as f:
    data.extend([line[2:] for line in f.readlines()])   # First two characters for each line (class and whitepsace) are removed

def generate_and_tokenize_prompt(data_point):
    tokenized_full_prompt = tokenizer(data_point["Paragraph"].strip(), padding=True, truncation=True)
    return tokenized_full_prompt

dataset = pd.DataFrame(data[:16], columns=["Paragraph"])
dataset = Dataset.from_pandas(dataset)
dataset = dataset.shuffle().map(generate_and_tokenize_prompt)

generation_config = model.generation_config
generation_config.temperature = 0.7
generation_config.top_p = 0.7
generation_config.pad_token_id = tokenizer.eos_token_id
generation_config.eos_token_id = tokenizer.eos_token_id
generation_config.max_new_tokens = 400

# generation_config.num_return_sequences = 5    ## NOTEEE WHEN WE WANT MULTIPLE INDEPENDANT OUTPUTS IN THE FUTURE, WE SHOULD USE THIS CONFIGURATION

encoding = tokenizer("The capital of USA is", return_tensors="pt").to("cuda")
with torch.no_grad():
    outputs = model.generate(
        input_ids = encoding.input_ids,
        attention_mask = encoding.attention_mask,
        generation_config = generation_config
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))

training_args = transformers.TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    learning_rate=1e-4,
    fp16=True,
    output_dir="finetune_medicine",
    optim="paged_adamw_8bit",
    lr_scheduler_type="cosine",
    warmup_ratio=0.01,
    report_to="none"
)

trainer = transformers.Trainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False)
)
model.config.use_cache = False
trainer.train()

model.save_pretrained("finetuned-model")

PEFT_MODEL = "finetuned-model"

config = PeftConfig.from_pretrained(PEFT_MODEL)
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    return_dict=True,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

tokenizer=AutoTokenizer.from_pretrained(config.base_model_name_or_path)
tokenizer.pad_token = tokenizer.eos_token

model = PeftModel.from_pretrained(model, PEFT_MODEL)

prompt = "Symptoms: I am having severe stomach inflammation and burping. Tell me the reason for this!\n Disease OR Condition: ".strip()

device = "cuda"
encoding = tokenizer(prompt, return_tensors="pt").to(device)
with torch.inference_mode():
  outputs = model.generate(
      input_ids = encoding.input_ids,
      attention_mask = encoding.attention_mask,
      generation_config = generation_config
  )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))




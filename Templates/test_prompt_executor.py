import template_prompt
import prompt_examples

if __name__ == "__main__":
    chat_prompt = template_prompt.get_chat_prompt()
    chat_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptopms="I have a runny nose and a cough")
    print(chat_prompt)

    #TODO: @ShreeSinghi change the hardcoded prompt to auto-generated refined example prompt
    #Hardcoded prompt for refined example for now
    refined_prompt = template_prompt.get_refined_prompt2(prompt_examples.get_refined_example_prompt1())
    refined_prompt.format_messages(name="HealO", background="I am a 20 year old male", symptopms="I have a runny nose and a cough")
    print(refined_prompt)

# get_refined_prompt2



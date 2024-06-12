import template_prompt

if __name__ == "__main__":
    chat_prompt = template_prompt.get_chat_prompt()
    chat_prompt.format_messages(name="HealO", user_input="What is the best way to treat a cold?")
    print(chat_prompt)





from langchain_core.prompts import ChatPromptTemplate
from utils import get_llm_model

model = get_llm_model("ollama-llama3.1")

template = """
You are an Assistant, answer the user question below be concise and don't make up answers if you don't have 
sufficient information

Here is the chat history : {context}

User question : {user_q}
"""
prompt_template = ChatPromptTemplate.from_template(template)

context = []

def chat_function(user_input:str, context:str) -> str:
    """
    Takes the user query and context 
    Get response from llm and 
    Return bot response
    """
    chain = prompt_template | model 
    bot_response = chain.invoke({"user_q":user_input, "context":context})
    return bot_response

def chat_handler(user_input:str) -> str:
    """
    Get user query
    Invoke chat function and get bot response
    Add user question and response to context
    Return bot response
    """
    context_str = "\n".join(c for c in context)
    bot_response = chat_function(user_input, context_str)
    context.append(f"user : {user_input}")
    context.append(f"bot : {bot_response}")
    return bot_response


if __name__ == "__main__":
    print("Welcome to ollama bot, press 'Q' to exit!")
    while True:
        user_input = input("Enter your question : ")
        if user_input.lower() == 'q':
            print("Bye...")
            break
        bot_response = chat_handler(user_input)
        print(bot_response)
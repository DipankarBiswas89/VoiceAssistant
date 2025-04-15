from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
#from langchain.chains import LLMChain
from decouple import config

def handle_query(user_input):
    try:
        llm = ChatGroq(
            groq_api_key=config('GROQ_API_KEY'),
            model_name="llama3-8b-8192"
        )
        prompt_template = PromptTemplate(
            input_variables=["input"],
            template="You are a helpful voice assistant. Respond to: {input}"
        )
        prompt = prompt_template.format(user_input=user_input)
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error processing query: {str(e)}"
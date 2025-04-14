from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from decouple import config

def handle_query(user_input):
    try:
        llm = ChatGroq(
            groq_api_key=config('GROQ_API_KEY'),
            model_name="mixtral-8x7b-32768"
        )
        prompt = PromptTemplate(
            input_variables=["input"],
            template="You are a helpful voice assistant. Respond to: {input}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run(input=user_input)
        return response
    except Exception as e:
        return f"Error processing query: {str(e)}"
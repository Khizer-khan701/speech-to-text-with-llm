from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def predict_category(text: str):
    prompt = ChatPromptTemplate.from_template("""
    You are an intelligent text classifier. 
    Analyze the following input text and infer the most likely categories it belongs to. 
    Categories should be general domains like Sports, Technology, Education, Health, Entertainment, Politics, etc.
    
    Input text: "{text}"

    Return the top 3 categories with confidence scores between 0 and 1 in JSON format:
    {{
      "categories": [
        {{"name": "Category1", "confidence": 0.xx}},
        {{"name": "Category2", "confidence": 0.xx}},
        {{"name": "Category3", "confidence": 0.xx}}
      ]
    }}
    """)

    chain = prompt | llm
    response = chain.invoke({"text": text})
    return response.content

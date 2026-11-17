from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    ("human", "{question}"),
])
model = ChatCohere()
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

input = {"question": "What is the capital of Peru?","system_message": "You are a helpful assitant who stictly gives one word answer."}
# Run it
result = chain.invoke(input)
print(result)

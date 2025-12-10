import datetime
import os
from langchain_openai import ChatOpenAI

from src.types.query_types import QueryIntent
from src.nlu_system.prompt import query_intent_generation_prompt_template as prompt
from src.nlu_system.query_examples import example_str




def generate_query_intent(user_input: str, data_schema: dict) -> QueryIntent:
    """Generates a QueryIntent from user input using a language model and structured output."""
    # TODO: move to config, add more settings such as reasoning effort
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    
    structured_llm = llm.with_structured_output(QueryIntent)
    chain = prompt | structured_llm

    data_schema_str = "\n".join([f"- {col}: {dtype}" for col, dtype in data_schema.items()])
    result: QueryIntent = chain.invoke({"input": user_input, 
                                        "examples": example_str, 
                                        "data_schema": data_schema_str,
                                        "current_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")})
    return result

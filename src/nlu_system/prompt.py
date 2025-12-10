from langchain_core.prompts import ChatPromptTemplate

"""
In this prompt we define how to translate user input into a structured JSON query.
Examples are provided as a variable, since it must be compliant with pydantic types which might change over time.
Examples come before data schema, as they are less likely to change which helps with caching.
"""

# TODO: file based prompt management if prompts grow in size/complexity
template = """
Your task is to translate users input in natural language to a JSON representing query.

Examples:
{examples}

Data schema:
{data_schema}

Today's date is: {current_date}

User Input:
{input}
"""

query_intent_generation_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", template),
    ]
)

# How to run
## Prerequisites:
`uv` installed. Required for project management.

## Steps
After cloning this repo you should run:
```
uv sync
```

Make sure to fill in your OPENAI API key in `.env` file.
You could rename `.env_example` to `.env` and insert your key as prompted.

Make sure the virtual environment is active, then you should be ready to run from the project root:
```
python main.py --query "Show me all vehicles with battery health below 85%"
```

Example output:

```
Generating query...

Generated QueryIntent:  query_plan='Filter for battery_health_percent < 85% and return all matching vehicles.' filters=[FilterCondition(column='battery_health_percent', operator=<FilterOperator.LT: '<'>, value=85)] sort_by=None sort_order=<SortOrder.NONE: 'none'> limit=None

Executing query...

Query Results:
+----+--------------+----------------------+--------------------------+---------------+
|    | vehicle_id   | timestamp            |   battery_health_percent |   odometer_km |
|----+--------------+----------------------+--------------------------+---------------|
|  0 | CAR001DPBHSA | 2024-11-20T09:00:00Z |                     77.4 |        115326 |
|  1 | CAR027BXXC02 | 2024-11-14T07:00:00Z |                     75.7 |        123180 |
... 
(Cut off output for clarity)
```

# Why you chose your approach
My approach to querying the "database" with natural language works by defining schema describing supported queries, having the LLM produce an object representing a query and handling the query execution programmatically.

Alternative approach is to allow the LLM write code and execute it for example in docker.

I chose to this approach because:

1. Security and safety concerns are mitigated. We don't need to setup up isolated environment to run unsafe, LLM code.
2. Type safety achieved via pydantic schemas. We can control what kind of queries are supported by controlling the schema.
3. Decoupling NLU from query execution allows to replace the query executor using any DBMS. Pandas should probably treated as a temporary, easy to use option rather than production ready solution.



# What you'd improve with more time (~200 words)
I would add more complex query options, such as chaining and nesting of the queries.
I would replace pandas with a more robust solution.
I would enforce column names to be compliant with the schema by dynamical generation of the LLM output's schema.
I would create a project config, in which the LLM parameters would be controlled.
User input should be sanitized and checked for prompt injection. Right now I pass the user input as a part of the system message, which is a bad design. It shoulld be marked as user input, which would trigger server-side evaluation by OpenAI API.
I also believe that tests could be improved by having an end-to-end test, in which LLM response is patched.

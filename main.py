from tabulate import tabulate
import dotenv
import argparse

from src.locator import get_data_dir
from src.nlu_system.query_generation import generate_query_intent
from src.load_data import load_data
from src.query_engine import QueryEngine

dotenv.load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Run natural language query on vehicle telemetry data.")
    parser.add_argument('--query', type=str, required=True, help='Query to execute, e.g. "Show me all vehicles with battery health below 85%"')
    args = parser.parse_args()

    user_input = args.query

    data_path = get_data_dir() / "telemetry.json"
    df = load_data(data_path)

    data_schema = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}

    print("Generating query...\n")
    query_intent = generate_query_intent(user_input, data_schema)
    print("Generated QueryIntent:\n", query_intent, "\n")

    print("Executing query...\n")
    query_engine = QueryEngine(df)
    result_df = query_engine.execute_query(query_intent)

    print("Query Results:")
    print(tabulate(result_df, headers='keys', tablefmt='psql', showindex=True))

if __name__ == "__main__":
    main()

import json
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def interpret_question(question: str, df_columns):
    """
    Converts a natural language question into a structured query for any dataset.
    """
    prompt = f"""
    You are a data analyst assistant.
    You are given a pandas DataFrame with columns: {list(df_columns)}
    Your task: Translate the natural language question into a structured JSON query that describes:
    - operation: sum, mean, max, min, count, top, unique_count, metadata
    - columns: which columns to use for aggregation
    - filter: conditions to filter rows (any column)
    - group_by: optional column for grouping
    - top_n: optional integer for top N results
    - metadata_key: optional, required if operation is 'metadata'

    Examples:
    - "Top 5 products by sales in 2023?" →
    {{ "operation": "top", "columns": ["Sales"], "filter": {{ "Year": [2023,2023] }}, "group_by": "Product", "top_n": 5 }}
    - "Number of unique customers in 2022?" →
    {{ "operation": "unique_count", "columns": ["CustomerID"], "filter": {{ "Year": [2022,2022] }} }}
    - "Total revenue for electronics?" →
    {{ "operation": "sum", "columns": ["Revenue"], "filter": {{ "Category": "Electronics" }} }}

    Question: {question}

    Respond ONLY in valid JSON. Do not include explanations or extra text.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    # Remove Markdown code block if present
    if raw_text.startswith("```") and raw_text.endswith("```"):
        raw_text = "\n".join(raw_text.split("\n")[1:-1]).strip()

    try:
        structured_query = json.loads(raw_text)
        return structured_query
    except Exception as e:
        return {"error": f"Failed to parse Gemini response: {e}", "raw": raw_text}

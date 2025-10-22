import pandas as pd
from interpret_question import interpret_question
from execute_query import execute_query
from logger_utils import log_interaction 

class DataAgent:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the agent with any dataframe.
        Creates a copy to avoid modifying the original data.
        """
        self.df = df.copy()

    def ask(self, question: str):
        # Step 1: Interpret the question
        query_dict = interpret_question(question, df_columns=self.df.columns)

        # Step 2: Execute the query
        answer = execute_query(self.df, query_dict)

        # Step 3: Log the question, structured query, and answer
        try:
            log_interaction(question, query_dict, answer)
        except:
            pass  # If logging fails, we just ignore

        return answer

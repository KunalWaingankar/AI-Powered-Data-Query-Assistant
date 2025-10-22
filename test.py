import pandas as pd
from data_agent import DataAgent
import preprocessor

#df = pd.read_csv("athlete_events.csv")
#region_df = pd.read_csv("noc_regions.csv")
stocks = pd.read_csv("Stocks.csv")
#df_clean = preprocessor.preprocess(df, region_df)

agent = DataAgent(stocks)

q1 = """Which stock has the highest average price in 2020?"""
print(q1)
print(agent.ask(q1))

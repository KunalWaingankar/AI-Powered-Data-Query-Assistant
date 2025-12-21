import streamlit as st
import pandas as pd
from data_agent import DataAgent
import preprocessor
import os

# -------------------------------
# Load & preprocess your dataset
# -------------------------------
st.title("📊 Natural Language Data Query Agent")

st.write("Ask questions like:")
st.code("""
1.) Number of Gold medals won by Germany in 2008?
2.) How many medals did India win in 2016?
3.) What was the average price of AAPL in 2020?
""")

#st.write(
 #   "API KEY FOUND:",
  #  os.environ.get("GEMINI_API_KEY") is not None
#)

st.write("API KEY FOUND:", "GEMINI_API_KEY" in st.secrets)

# Load dataset
df = pd.read_csv("https://huggingface.co/datasets/kunalwaingankar/olympic-project-files/resolve/main/athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")
stocks = pd.read_csv("Stocks.csv")
df_clean = preprocessor.preprocess(df, region_df)

# Create your agent
agent = DataAgent(df_clean)
agent1 = DataAgent(stocks)

# User input
question = st.text_input("Ask your question:")

if question:
    with st.spinner("Thinking..."):
        answer = agent.ask(question)

    st.subheader("🟦 Answer:")
    st.write(answer)

    # If the answer is a DataFrame → show nicely
    if isinstance(answer, pd.DataFrame):
        st.dataframe(answer)

    st.success("Query executed successfully!")









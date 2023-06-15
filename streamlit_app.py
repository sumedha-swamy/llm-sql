import streamlit as st
import os
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from pathlib import Path
import sqlalchemy as sa
from utils import get_redshift_endpoint
from prompt_templates import (
    get_generate_sql_template,
    get_generate_visualization_template,
)


def main():
    load_dotenv()

    redshift_endpoint = get_redshift_endpoint()
    engine = sa.create_engine(redshift_endpoint)
    conn = engine.connect()

    prompt_generate_sql = get_generate_sql_template()
    prompt_generate_visualization = get_generate_visualization_template()

    table_info = Path(os.environ["REDSHIFT_SIMPLE_SCHEMAFILE"]).read_text()

    st.header("Query Redshift database")
    query = st.text_input(
        "Enter your query in natural language", placeholder="What is the average sales price of tickets sold?"
    )

    if query:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", verbose=True)

        # Generate the SQL Query corresponding to the user prompt
        llm_chain_generate_sql = LLMChain(llm=llm, prompt=prompt_generate_sql)
        output_sql = llm_chain_generate_sql.predict(
            input=query, dialect="redshift", table_info=table_info
        )

        st.caption("SQL Query to answer the question")
        st.code(output_sql, language="sql")

        # Execute the SQL code on Redshift
        result = conn.execute(output_sql)
        result_lst = [r for r in result]

        st.caption("Result")
        st.code(result_lst, language="sql")

        # Generate python code to visualize the output
        llm_chain_generate_visualization = LLMChain(
            llm=llm, prompt=prompt_generate_visualization
        )
        output_visualization = llm_chain_generate_visualization.predict(
            input_data=output_sql, sql_query=output_sql
        )

        st.caption("Python code to visualize the data")
        st.code(output_visualization, language="python")


if __name__ == "__main__":
    main()

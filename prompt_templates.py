from langchain import PromptTemplate

TEMPLATE_GENERATE_SQL = """Given an input question, create a syntactically correct {dialect} query to run.


    Only use the tables listed below. The structure of the tables listed below is in the format: schema name| table name| column name| data type|:

    Tables to use:

    {table_info}


    Input Question: {input}"""


def get_generate_sql_template():
    prompt_generate_sql = PromptTemplate(
        input_variables=["input", "table_info", "dialect"],
        template=TEMPLATE_GENERATE_SQL,
    )
    return prompt_generate_sql


TEMPLATE_GENERATE_VISUALIZATION = """Given input data, create a syntactically correct python script to generate the most appropriate visualization for the data. Assume that the data in stored in a dataframe named data_from_sql. Assume that the connection object to connect to the database is named conn


    The SQL query used to generate the data is: {sql_query}


    Input Data: {input_data}"""


def get_generate_visualization_template():
    prompt_generate_visualization = PromptTemplate(
        input_variables=["input_data", "sql_query"],
        template=TEMPLATE_GENERATE_VISUALIZATION,
    )
    return prompt_generate_visualization

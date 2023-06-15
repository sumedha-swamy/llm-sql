from dotenv import load_dotenv
import os
import sqlalchemy as sa
from utils import get_redshift_endpoint

load_dotenv()

# Connect to Redshift
redshift_endpoint = get_redshift_endpoint()
engine = sa.create_engine(redshift_endpoint)
conn = engine.connect()

# Fetch names of all schemas and tables in the database
result = conn.execute(
    "SELECT schemaname, tablename FROM pg_catalog.pg_tables \
    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema' \
    GROUP BY schemaname,tablename; "
)

# Put the result into "schema.tablename" format
# While results improve when sending the table schema definitions,
# the size of inputs to the LLM can be large. Consider optimizing
# the subset of schema data sent to the LLM
tables = [f"{r[0]}.{r[1]}" for r in result]

# Write the DDL of the tables into REDSHIFT_SCHEMAFILE
with open(os.environ["REDSHIFT_SCHEMAFILE"], "w") as fp:
    for table in tables:
        result = conn.execute(f"SHOW TABLE {table};")
        ddl = [r[0] for r in result]
        fp.write("%s\n" % ddl)

# Write the simple table structure into REDSHIFT_SIMPLE_SCHEMAFILE
# in the format schema name| table name| column name| data type|
# Note: The schemas can be large. Consider limiting the set of tables
# you will send to the LLM. Using FAISS did not seem to help with this
# data format
result_columns = conn.execute(
    "SELECT table_schema, table_name, column_name,\
                                data_type FROM information_schema.columns\
                                WHERE table_schema != 'pg_catalog' AND \
                                table_schema != 'information_schema' AND table_name='titanic'\
                                ;"
)
columns = [f"{r[0]}|{r[1]}|{r[2]}|{r[3]}|\\n" for r in result_columns]

with open(os.environ["REDSHIFT_SIMPLE_SCHEMAFILE"], "w") as fp:
    for c in columns:
        fp.write(c)

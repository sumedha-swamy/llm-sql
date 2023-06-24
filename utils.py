import os


def get_redshift_endpoint() -> str:
    username = os.environ["REDSHIFT_USERNAME"]
    password = os.environ["REDSHIFT_PASSWORD"]
    host = os.environ["REDSHIFT_HOST"]
    port = os.environ["REDSHIFT_PORT"]
    database = os.environ["REDSHIFT_DATABASE"]
    redshift_endpoint = f"redshift+psycopg2://{username}:{password}@{host}:{port}/{database}"
    return redshift_endpoint

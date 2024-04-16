from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy

# helper function to return SQLAlchemy connection pool
def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
    # function used to generate database connection
    def getconn() -> pymysql.connections.Connection:
        conn = connector.connect(
            "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
            "pymysql",
            user="root",
            password="1234",
            db="allcontentdatabase"
        )
        return conn

    # create connection pool
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    return pool

# initialize Cloud SQL Python Connector as context manager
with Connector() as connector:
    # initialize connection pool
    pool = init_connection_pool(connector)
    # insert statement

    # interact with Cloud SQL database using connection pool
    with pool.connect() as db_conn:

        # query database
        result = db_conn.execute(sqlalchemy.text("SELECT * from Songs LIMIT 10")).fetchall()

        # Do something with the results
        for row in result:
            print(row)
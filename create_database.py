import mysql.connector
#import pandas as pd

#df_spotify = pd.read_csv('/spotify.csv')
#df_spotify.to_json("/spotify.json",orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=2)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='1234'
)

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
databases = mycursor.fetchall()
print(databases)
desired_databases = {'nonduplicatesongsdatabase','usersdatabase','allcontentdatabase'}

# Check if the databases exists
for desired_database in desired_databases:
    db_exists = any(desired_database in db for db in databases)
    if not db_exists:
        mycursor.execute(f"CREATE DATABASE {desired_database}")
        print(f"Database '{desired_database}' created successfully")
    else:
        print(f"Database '{desired_database}' already exists")

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='1234',
        database='nonduplicatesongsdatabase'
    )
print("Connected to database 'nonduplicatesongsdatabase'")
mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS  Songs")
mycursor.execute('''CREATE TABLE Songs (
        song_id INTEGER AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(245),
        `rank` INTEGER,
        date DATE,
        artist VARCHAR(245),
        url VARCHAR(245),
        region VARCHAR(245),
        chart VARCHAR(245),
        trend VARCHAR(245),
        streams INTEGER
    )
''')
mydb.commit()
print("Table Songs created!")
mydb.close()


mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='1234',
        database='usersdatabase'
    )
print("Connected to database 'usersdatabase'")
mycursor = mydb.cursor()


mydb.close()



mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='1234',
        database='allcontentdatabase'
    )
print("Connected to database 'allcontentdatabase'")
mycursor = mydb.cursor()


mydb.close()



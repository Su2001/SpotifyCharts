import mysql.connector
import pandas as pd
import os

df_spotify = pd.read_csv('charts.csv')
# Check if df_spotify exists
if df_spotify is None:
    print("Error: df_spotify does not exist")
    exit()
# Check if charts.json exists before creats it
if 'charts.json' not in os.listdir():
    df_spotify.to_json("charts.json",orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=2)
    print("File 'charts.json' created successfully")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='1234'
)

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
databases = mycursor.fetchall()
desired_databases = {'nonduplicatesongsdatabase','usersdatabase','allcontentdatabase'}

# Check if the databases exists
for desired_database in desired_databases:
    db_exists = any(desired_database in db for db in databases)
    if not db_exists:
        mycursor.execute(f"CREATE DATABASE {desired_database}")
        print(f"Database '{desired_database}' created successfully")
    else:
        print(f"Database '{desired_database}' already exists")

# Connect to the allcontentdatabase
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='1234',
        database='allcontentdatabase'
    )
print("Connected to database 'allcontentdatabase'")
mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS  Songs")
mycursor.execute('''CREATE TABLE Songs (
        song_id INTEGER AUTO_INCREMENT PRIMARY KEY,
        title TEXT,
        `rank` INTEGER,
        date DATE,
        artist TEXT,
        url VARCHAR(245),
        region VARCHAR(245),
        chart VARCHAR(245),
        trend VARCHAR(245),
        streams INTEGER
    )
''')
mydb.commit()
sql_query = '''INSERT INTO Songs (title, `rank`, date, artist, url, region, chart, trend, streams) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

# Convert the DataFrame to a list of tuples
songs_list = [tuple(x) for x in df_spotify.values]

# Define the chunk size
chunk_size = 100000

# Insert the data in chunks
for i in range(0, len(songs_list), chunk_size):
    chunk = songs_list[i:i+chunk_size]
    mycursor.executemany(sql_query, chunk)
    print("index",i)
    mydb.commit()

print("Data inserted into table Songs in allcontentdatabase")
mydb.close()

# Connect to the nonduplicatesongsdatabase
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
        title TEXT,
        `rank` INTEGER,
        date DATE,
        artist TEXT,
        url VARCHAR(245),
        region VARCHAR(245),
        chart VARCHAR(245),
        trend VARCHAR(245),
        streams INTEGER
    )
''')
mydb.commit()
print("Table Songs created!")
df_spotify_unique = df_spotify.drop_duplicates(subset=['title', 'artist'])
songs_list = [tuple(x) for x in df_spotify_unique.values]
sql_query = '''INSERT INTO Songs (title, `rank`, date, artist, url, region, chart, trend, streams) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
mycursor.executemany(sql_query, songs_list)
mydb.commit()
print("Data inserted into table Songs in nonduplicatesongsdatabase")
mydb.close()


# Connect to the usersdatabase
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='1234',
        database='usersdatabase'
    )
print("Connected to database 'usersdatabase'")
mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS  playlists")
mycursor.execute("DROP TABLE IF EXISTS  users")
mycursor.execute("""
    CREATE TABLE users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255)
    )
""")
print("Table 'users' created successfully")

mycursor.execute("DROP TABLE IF EXISTS  playlists")
# Create 'playlists' table
mycursor.execute("""
    CREATE TABLE playlists (
        playlist_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        song_id INT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
""")
print("Table 'playlists' created successfully")

mydb.close()






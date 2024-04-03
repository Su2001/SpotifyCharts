import mysql.connector
import pandas as pd
import os
import json
from google.cloud import storage

# Define the Google Cloud Storage bucket and JSON file path
bucket_name = 'spotifychartsgroup01bucket'
file_low_data_path = 'charts_low_data.json'
file_full_data_path = 'charts.json'

# Initialize a client
storage_client = storage.Client()

# Get the bucket
bucket = storage_client.get_bucket(bucket_name)

# Get the blob (file) from the bucket
blob = bucket.blob(file_low_data_path)

# Download the JSON data as a string
json_data = blob.download_as_string()

# Decode the JSON string
json_data_decoded = json_data.decode('utf-8')

# Load the JSON data into a Python dictionary
data_dict = json.loads(json_data_decoded)

# Convert the dictionary into a Pandas DataFrame
df_spotify = pd.DataFrame(data_dict)

mydb = mysql.connector.connect(
    host="172.21.0.2",
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
        host="172.21.0.2",
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
        host="172.21.0.2",
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
        artist TEXT,
        url VARCHAR(245),
        numtimesincharts INTEGER,
        numcountrydif INTEGER
    )
''')
mydb.commit()
print("Table Songs created!")
mycursor.execute("DROP TABLE IF EXISTS  Comments")
mycursor.execute('''CREATE TABLE Comments (
        comment_id INTEGER AUTO_INCREMENT PRIMARY KEY,
        user_id INTEGER,
        song_id INTEGER,
        comment TEXT
        )
''')
mydb.commit()
print("Table Comments created!")
comments_list = [
    (1, 1, "Great song!"),
    (2, 1, "Love it!"),
    (3, 2, "Awesome track!"),
    (4, 3, "This song is fire!")
]
sql_query = '''INSERT INTO Comments (user_id, song_id, comment) VALUES (%s, %s, %s)'''
mycursor.executemany(sql_query, comments_list)
mydb.commit()
print("Data inserted into table Comments in nonduplicatesongsdatabase")

df_spotify_unique = df_spotify.drop_duplicates(subset=['title', 'artist']).copy()
# Calculate numtimesincharts and numcountrydif
numtimesincharts = df_spotify.groupby(['title', 'artist']).size().reset_index(name='numtimesincharts')
numcountrydif = df_spotify.groupby(['title', 'artist'])['region'].nunique().reset_index(name='numcountrydif')

# Merge df_spotify_unique with numtimesincharts and numcountrydif
df_spotify_unique = pd.merge(df_spotify_unique, numtimesincharts, on=['title', 'artist'])
df_spotify_unique = pd.merge(df_spotify_unique, numcountrydif, on=['title', 'artist'])

songs_list = [(x['title'], x['artist'], x['url'], x['numtimesincharts'], x['numcountrydif']) for x in df_spotify_unique.to_dict('records')]
sql_query = '''INSERT INTO Songs (title, artist, url, numtimesincharts, numcountrydif) VALUES (%s, %s, %s, %s, %s)'''

mycursor.executemany(sql_query, songs_list)
mydb.commit()
print("Data inserted into table Songs in nonduplicatesongsdatabase")
mydb.close()


# Connect to the usersdatabase
mydb = mysql.connector.connect(
        host="172.21.0.2",
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
mydb.commit()

users_list = [
    ('Bruno', 'Bruno@example.com', 'password123'),
    ('Su', 'Su@example.com', 'password456'),
    ('Ana', 'Ana@example.com', 'password789'),
    ('Daniel', 'Daniel@example.com', 'password000')
]

sql_query = '''INSERT INTO users (username, email, password) VALUES (%s, %s, %s)'''
mycursor.executemany(sql_query, users_list)
mydb.commit()
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
mydb.commit()
print("Table 'playlists' created successfully")
# Insert examples into 'playlists' table
playlists_list = [
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 1),
    (4, 2)
]

sql_query = '''INSERT INTO playlists (user_id, song_id) VALUES (%s, %s)'''
mycursor.executemany(sql_query, playlists_list)
mydb.commit()

print("Data inserted into table playlists in usersdatabase")

mydb.close()






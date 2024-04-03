SpotifyChartsGroup1

How to run the project:
./build.sh

How to test the different use cases:
search(GET), after acessing the correspondent link for the use case add the following suffix after the .dev in the link:
      /regular/search?song=a
  <br>for example:
      https://5001-cs-314474093647-default.cs-europe-west1-xedi.cloudshell.dev/regular/search?song=a

topcharts(GET), after acessing the correspondent link for the use case add the following suffix after the .dev in the link:
      /regular/top-charts?date=2017-01-01&country=Argentina
  <br>for example:
      https://5001-cs-314474093647-default.cs-europe-west1-xedi.cloudshell.dev/regular/top-charts?date=2017-01-01&country=Argentina
      
song details(GET), after acessing the correspondent link for the use case add the following suffix after the .dev in the link:
      /regular/song-details/1
  <br>for example:
      https://5003-cs-314474093647-default.cs-europe-west1-xedi.cloudshell.dev/regular/song-details/1
      
comments(POST), it is possible to execute a POST through the following code, inserting it in the console:
      curl -i -X POST -H 'Content-Type: application/json' 'http://127.0.0.1:5000/premium/song-details/1/comment?user_id=1&comment=This%20is%20a%20test'
    <br>to check if the POST was successful you can check the song details of that certain song
    
comments(DELETE), it is possible to execute a DELETE through the following code, inserting it in the console:
      curl -i -X DELETE http://127.0.0.1:5000/premium/song-details/1/comment/1
    <br>to check if the DELETE was successful you can check the song details of that certain song

comments(PUT), it is possible to execute a PUT through the following code, inserting it in the console:
      curl -i -X PUT -H 'Content-Type: application/json'  'http://127.0.0.1:5000/premium/song-details/2/comment/3?user_id=3&comment=TESTESTES'
    <br>to check if the PUT was successful you can check the song details of that certain song
    
playlist(POST), it is possible to execute a POST through the following code, inserting it in the console:
      curl -i -X POST -H 'Content-Type: application/json' -d '{"user_id": "1"} http://127.0.0.1:8080/premium/playlist/1
    <br>to check you need to access the database and check the table

playlist(DELETE), it is possible to execute a DELETE through the following code, inserting it in the console:
      curl -i -X DELETE http://127.0.0.1:8080/premium/playlist/1?user_id=1
    <br>to check you need to access the database and check the table

playlist(GET), it is possible to execute a DELETE through the following code, inserting it in the console:
      curl -i -X DELETE http://127.0.0.1:8080/premium/playlist/1?user_id=1
    <br>to check you need to access the database and check the table

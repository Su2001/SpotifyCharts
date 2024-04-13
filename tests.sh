curl -i -X POST -H 'Content-Type: application/json'  'http://127.0.0.1:5000/premium/song-details/2/comment?user_id=3&comment=Grupo01'
curl -i -X PUT -H 'Content-Type: application/json'  'http://127.0.0.1:5000/premium/song-details/2/comment/3?user_id=3&comment=Updated'
curl -i -X DELETE http://127.0.0.1:5000/premium/song-details/1/comment/1?user_id=1

curl -i -X POST -H 'Content-Type: application/json' -d '{"user_id": "1"}' http://127.0.0.1:8080/premium/playlist/1
curl -i -X DELETE http://127.0.0.1:8080/premium/playlist/1?user_id=1
from playlist_pb2 import AddPlayListRequest, GetPlayListRequest, RemovePlayListRequest
import grpc
from playlist_pb2_grpc import AddPlayListStub, GetPlayListStub, RemovePlayListStub
channel = grpc.insecure_channel("localhost:50051")
client = AddPlayListStub(channel)
request = AddPlayListRequest(user_id = 2, song_id = 90)
client.Add(request)

channel1 = grpc.insecure_channel("localhost:50051")
client1 = RemovePlayListStub(channel1)
request1 = RemovePlayListRequest(user_id=2, song_id=90)
client1.Remove(request1)

channel2 = grpc.insecure_channel("localhost:50051")
client2 = GetPlayListStub(channel2)
request2 = GetPlayListRequest(user_id=2)
a = client2.Get(request2)
print(a.songs)





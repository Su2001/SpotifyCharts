from playlist_pb2 import ModifyPlayListRequest, GetPlayListRequest
from playlist_pb2_grpc import PlayListServiceStub
import grpc
channel = grpc.insecure_channel("localhost:50051")
client = PlayListServiceStub(channel)
request = ModifyPlayListRequest(user_id = 2, song_id = 90)
client.Add(request)

request1 = ModifyPlayListRequest(user_id=2, song_id=90)
client.Remove(request1)

request2 = GetPlayListRequest(user_id=2)
a = client.Get(request2)
print(a.songs)





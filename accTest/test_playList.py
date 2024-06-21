import pytest
import requests


# test get
x = requests.get('http://localhost:8080/premium/playlist/test?user_id=-1')
assert x.status_code == 200
assert x.text == "[100,34,65]\n"

x = requests.get('http://localhost:8080/premium/playlist/test?user_id=-2')
assert x.status_code == 200
assert x.text == "[1,2,3]\n"

x = requests.get('http://localhost:8080/premium/playlist/test?user_id=-10')
assert x.status_code == 500

#test post
url = 'http://localhost:8080/premium/playlist/test/1001'
myobj = {'user_id': -1}

x = requests.post(url, json= myobj)
assert x.status_code == 200

x = requests.get('http://localhost:8080/premium/playlist/test?user_id=-1')
assert x.status_code == 200
assert x.text == "[100,34,65,1001]\n"

#test post
url = 'http://localhost:8080/premium/playlist/test/1001?user_id=-1'

x = requests.delete(url)
assert x.status_code == 200

x = requests.get('http://localhost:8080/premium/playlist/test?user_id=-1')
assert x.status_code == 200
assert x.text == "[100,34,65]\n"

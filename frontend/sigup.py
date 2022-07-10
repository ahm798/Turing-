import requests
from getpass import getpass

username = input("username:   ")
password = getpass("password:   ")
email = input("email: ")
endpoint = 'http://127.0.0.1:8000/api/account/register/'

response = requests.post(endpoint, json={"username": username, 'password': password, 'email':email})



print(response.json())


# if response.status_code == 200:
#     token = response.json()['token']
#     headersv2 = {'authorization': f'token {token}'}
#     response_v2 = requests.post(endpoint, json=data,headers=headersv2)
#     print(response_v2.json())
import requests

headers = {'Authorization': 'VC a14343242300asdfgasdfafdsggsgsd'}
response = requests.get('http://localhost:9000', headers=headers)
print(response)
print(response.headers)

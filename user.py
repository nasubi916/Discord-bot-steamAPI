import requests

# Steam APIキーを設定する
api_key = '16CA8E11393C4043B83A6FE137BA20C3'

# SteamのユーザーIDを取得する
steam_id = input('Enter a Steam ID: ')

# Steam Web APIを呼び出し、ユーザーのプロフィールを取得する
url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}'
response = requests.get(url)
data = response.json()

# ユーザーのプロフィールを表示する
print(f'Profile: {data["response"]["players"][0]["personaname"]}')
print(f'Profile URL: {data["response"]["players"][0]["profileurl"]}')
print(f'Avatar: {data["response"]["players"][0]["avatarfull"]}')
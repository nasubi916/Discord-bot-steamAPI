import requests

# Steam Web APIキーを設定する
APIKey = '16CA8E11393C4043B83A6FE137BA20C3'

# Steamアプリのリストを取得する
response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
gameList = response.json()

# GameのApp IDを取得する
appID = None
appName = 'Muse Dash'
for game in gameList['applist']['apps']:
    if game['name'] == appName:
        appID = game['appid']
        print('ID:',game['name'], game['appid'])
        break

# ゲームが見つからない場合は、終了します。
if appID is None:
    print(f'Game not found')
    exit()
else:
    # Steam Web APIを呼び出し、ゲームの同時接続人数を取得する
    url = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?key={APIKey}&appid={appID}'
    response = requests.get(url)
    data = response.json()
    playerCount = data["response"]["player_count"]
    
    # 現在のプレイヤー数を表示する
    print(f'Player: {appName}: {playerCount}')

    # ゲーム名を入力してもらう
    inputGameName = input('Enter a game name: ')
    
    # 入力されたゲームの同時接続人数を取得する
    inputAppID = None
    for game in gameList['applist']['apps']:
        if game['name'] == inputGameName:
            inputAppID = game['appid']
            break
    
    if inputAppID is not None:
        # 入力されたゲームの同時接続人数を取得する
        url = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?key={APIKey}&appid={inputAppID}'
        response = requests.get(url)
        data = response.json()
        
        # 入力されたゲームの同時接続人数を表示する
        inputPlayerCount = data["response"]["player_count"]
        print(f'Player: {inputGameName}: {inputPlayerCount}')
        
        # 入力されたゲームの同時接続人数と、Muse Dashの同時接続人数を比較する
        if inputPlayerCount > playerCount:
            print(f'{inputGameName} has more players than {appName}.')
        elif inputGameName == appName:
            print(f'{inputGameName} and {appName} are the same game.')
        elif inputPlayerCount == playerCount:
            print(f'{inputGameName} has the same number of players as {appName}.')
        else:
            print(f'{appName} has more players than {inputGameName}.')
    else:
        print(f'Could not find game "{inputGameName}".')

import os
import random
import discord
import requests
from dotenv import load_dotenv

# インテントの生成
intents = discord.Intents.default()
intents.message_content = True
# クライアントの生成
client = discord.Client(intents=intents)

# .envファイルを読み込む
load_dotenv()
# Steam Web APIキーを設定する
APIKey = os.getenv('STEAM_API_KEY')
#ゲームリストを取得する
response = requests.get(
    'https://api.steampowered.com/ISteamApps/GetAppList/v2/')
gameList = response.json()

#定義
gameName = None
playerCount = 0
isUp=True

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # グローバル変数を使用する
    global gameName,playerCount,isUp
    # 自分のメッセージを無効
    if message.author == client.user:
        return

    # メッセージが"!hello"で始まっていたら"Hello!"と応答
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')


    # メッセージが"!quiz"で始まっていたらクイズを開始する
    if message.content.startswith('!quiz'):
        #上か下かを決める
        isUp=random.randint(0,1)
        #これ上位10位のゲームにしてもいいかも
        gamesList=['Muse Dash','Beat Saber','Apex Legends','Wallpaper Engine','Destiny 2','Dota 2','Counter-Strike: Global Offensive',
        'ARK: Survival Evolved','CODE VEIN','Battlefield™ 2042','Terraria','Pogostuck:Raga With Your Friends','Getting Over It with Bennett Foddy','Celeste']

        # ランダムに選ばれたゲームのApp IDを取得する
        appID = None
        gameName = random.choice(gamesList)
        for game in gameList['applist']['apps']:
            if game['name'] == gameName:
                appID = game['appid']
                break
        # Steam Web APIを呼び出し、ゲームの同時接続人数を取得する
        if appID is not None:
            url = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?key={APIKey}&appid={appID}'
            response = requests.get(url)
            data = response.json()
            playerCount = data["response"]["player_count"]
            # 現在のプレイヤー数を表示する
            await message.channel.send(f'Now: {gameName} {playerCount}')
            if isUp==True:
                await message.channel.send(f'{gameName}のプレイヤー数は{playerCount}人です。これよりも多いゲーム"!answer"で入力してください。')
            else:
                await message.channel.send(f'{gameName}のプレイヤー数は{playerCount}人です。これよりも少ないゲーム"!answer"で入力してください。')



    # 入力されたゲームの同時接続人数を取得する
    if message.content.startswith('!answer'):
        #gameNameがNoneの場合は、終了します。
        if gameName is None:
            await message.channel.send(f'gameName is None\n先に"!quiz"を実行してください。')
            return

        # 入力されたゲームの名前を取得する
        inputGameName = message.content.split('!answer ')[1]
        # 入力されたゲームのIDを取得する
        inputGameID = None
        if inputGameName is not None:
            for game in gameList['applist']['apps']:
                if game['name'] == inputGameName:
                    inputGameID = game['appid']
                    break

        # ゲームの名前が見つからない場合は、終了します。
        if inputGameName is None:
            await message.channel.send(f'inputGameName not found')
            return
        # ゲームのIDが見つからない場合は、終了します。
        if inputGameID is None:
            await message.channel.send(f'inputGameID not found')
            return

        # 入力されたゲームの同時接続人数を取得する
        url = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?key={APIKey}&appid={inputGameID}'
        response = requests.get(url)
        data = response.json()
        # 入力されたゲームの同時接続人数を表示する
        inputPlayerCount = data["response"]["player_count"]
        await message.channel.send(f'Now: {inputGameName} {inputPlayerCount}')

        # 入力されたゲームの同時接続人数と、ランダムに選ばれたゲームの同時接続人数を比較する
        if inputPlayerCount > playerCount:
            await message.channel.send(f"{inputGameName} は {gameName} よりも多くのプレイヤーがいるので、、、")
            if isUp:
                await message.channel.send("正解です。")
            else:
                await message.channel.send("不正解です。")
        elif inputPlayerCount < playerCount:
            await message.channel.send(f"{gameName} は {inputGameName} よりも多くのプレイヤーがいるので、、、")
            if isUp:
                await message.channel.send("不正解です。")
            else:
                await message.channel.send("正解です。")
        else:
            await message.channel.send(f"{inputGameName} と {gameName} は同じ数のプレイヤーがいます。")


    #ヘルプの表示する
    if message.content.startswith('!help'):
        await message.channel.send(f'!help : このメッセージを表示します。\n!hello: Hello!と応答します。\n!quiz : クイズを開始します。\n!answer [ゲーム名] : "quiz"の回答をします。')

# クライアントの実行
client.run(os.getenv('DISCORD_TOKEN'))

#Rust、Grand Theft AutoⅤとかがなぜか取得できない。
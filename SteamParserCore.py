import json, urllib3, openpyxl
from openpyxl import Workbook
from datetime import datetime

STEAM_API_KEY = 'YOUR_STEAM_API_KEY'

SteamApi = urllib3.PoolManager()

SteamApiUserId = STEAM_USER_ID

SteamApiUrl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + STEAM_API_KEY + '&steamids=' + str(SteamApiUserId)

SteamApiData = SteamApi.request('GET', SteamApiUrl)
SteamApiData = SteamApiData.data.decode('utf-8')

#SteamApiData = json.dumps(SteamApiData)
SteamApiData = json.loads(SteamApiData)

for Player in SteamApiData["response"]["players"]:

    print(Player["steamid"], Player["personaname"])
    
    PlayerStatus = int(Player["personastate"])
    if PlayerStatus == 0:
        print('Offline')
        PlayserStatusText = 'Offline'
    elif PlayerStatus == 1:
        print('Online')
        PlayserStatusText = 'Online'
    elif PlayerStatus == 2:
        print('Busy')
        PlayserStatusText = 'Busy'
    elif PlayerStatus == 3:
        print('Away')
        PlayserStatusText = 'Away'
    elif PlayerStatus == 4:
        print('Snooze')
        PlayserStatusText = 'Snooze'
    elif PlayerStatus == 5:
        print('looking to trade')
        PlayserStatusText = 'looking to trade'
    elif PlayerStatus == 6:
        print('looking to play')
        PlayserStatusText = 'looking to play'
    else:
        print('Error')
        PlayserStatusText = 'Error'

    try:
        print(Player["gameid"], Player["gameextrainfo"])
        PlayerGameId = Player["gameid"]
        PlayerGameExtraInfo = Player["gameextrainfo"]
    except:
        print("No data about game")
        PlayerGameId = ' '
        PlayerGameExtraInfo = ' '

    try:
        print(Player["gameserverip"])
        PlayerGameServerIp = Player["gameserverip"]
    except:
        print("No data about server user currently playing")
        PlayerGameServerIp = ' '

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

ExcelTitle = ['year', 'month', 'day', 'hour', 'min', 'steamid', 'name', 'statuscode','status', 'gameid', 'gameinfo', 'gameserverip']
ExcelStatsRow = [datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'), 
                datetime.now().strftime('%H'), datetime.now().strftime('%M'),
                Player["steamid"], Player["personaname"], Player["personastate"], PlayserStatusText, PlayerGameId, PlayerGameExtraInfo, PlayerGameServerIp]

def createExcelFile():
    cr_Wb = Workbook()
    cr_Ws = cr_Wb.active
    cr_Ws.append(ExcelTitle)
    cr_Wb.save(str(SteamApiUserId)+'.xlsx')

def appendExcelStatsRow():
    curExcel = openpyxl.load_workbook(str(SteamApiUserId)+'.xlsx')
    curExcelWs = curExcel.active
    curExcelWs.append(ExcelStatsRow)
    curExcel.save(str(SteamApiUserId)+'.xlsx')

try:
    appendExcelStatsRow()
except:
    createExcelFile()
    print('New user, created a new excel file')
    appendExcelStatsRow()


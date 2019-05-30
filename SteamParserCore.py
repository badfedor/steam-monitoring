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
    elif PlayerStatus == 1:
        print('Online')
    elif PlayerStatus == 2:
        print('Busy')
    elif PlayerStatus == 3:
        print('Away')
    elif PlayerStatus == 4:
        print('Snooze')
    elif PlayerStatus == 5:
        print('looking to trade')
    elif PlayerStatus == 6:
        print('looking to play')
    else:
        print('Error')

    try:
        print(Player["gameid"], Player["gameextrainfo"])
    except:
        print("No data about game")

    try:
        print(Player["gameserverip"])
    except:
        print("No data about server user currently playing")

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

ExcelTitle = ['year', 'month', 'day', 'hour', 'min', 'steamid', 'name', 'status', 'gameid', 'gameinfo', 'gameserverip']

def createExcelFile():
    cr_Wb = Workbook()
    cr_Ws = cr_Wb.active
    cr_Ws.append(ExcelTitle)
    cr_Wb.save(str(SteamApiUserId)+'.xlsx')

try:
    curExcel = openpyxl.load_workbook(str(SteamApiUserId)+'.xlsx')
except:
    createExcelFile()
    print('ez')

import json, urllib3, openpyxl, threading
from openpyxl import Workbook
from datetime import datetime

STEAM_API_KEY = 'YOUR_STEAM_API_KEY'

SteamApi = urllib3.PoolManager()

SteamPlayersToMonitor = [STEAM_USER_IDS]

def GetPlayersInfo():

    threading.Timer(60.0, GetPlayersInfo).start()

    for SteamApiUserId in SteamPlayersToMonitor:

        SteamApiUrl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + STEAM_API_KEY + '&steamids=' + str(SteamApiUserId)

        SteamApiData = SteamApi.request('GET', SteamApiUrl)
        SteamApiData = SteamApiData.data.decode('utf-8')

        #SteamApiData = json.dumps(SteamApiData)
        SteamApiData = json.loads(SteamApiData)

        for Player in SteamApiData["response"]["players"]:
            
            PlayerStatus = int(Player["personastate"])
            if PlayerStatus == 0:
                PlayserStatusText = 'Offline'
            elif PlayerStatus == 1:
                PlayserStatusText = 'Online'
            elif PlayerStatus == 2:
                PlayserStatusText = 'Busy'
            elif PlayerStatus == 3:
                PlayserStatusText = 'Away'
            elif PlayerStatus == 4:
                PlayserStatusText = 'Snooze'
            elif PlayerStatus == 5:
                PlayserStatusText = 'looking to trade'
            elif PlayerStatus == 6:
                PlayserStatusText = 'looking to play'
            else:
                print('Error getting Status, Id: ' + str(SteamApiUserId))
                PlayserStatusText = 'Error'

            try:
                PlayerGameId = Player["gameid"]
                PlayerGameExtraInfo = Player["gameextrainfo"]
            except:
                PlayerGameId = ' '
                PlayerGameExtraInfo = ' '

            try:
                print(Player["gameserverip"])
                PlayerGameServerIp = Player["gameserverip"]
            except:
                PlayerGameServerIp = ' '

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
            print('New user, Id: ' + str(SteamApiUserId) + ', created a new excel file')
            appendExcelStatsRow()

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + 'Info get SUCCESS, users total: ' + str(len(SteamPlayersToMonitor)))

GetPlayersInfo()

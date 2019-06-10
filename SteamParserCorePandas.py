import json, urllib3, threading
import pandas as pd
from datetime import datetime

STEAM_API_KEY = 'YOUR_STEAM_API_KEY'
REQUEST_DELAY = 60

SteamApi = urllib3.PoolManager()

SteamPlayersToMonitor = ['STEAM_PLAYER_IDS']

def GetPlayersInfo():

    threading.Timer(int(REQUEST_DELAY), GetPlayersInfo).start()

    for SteamApiUserId in SteamPlayersToMonitor:

        SteamApiUrl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + STEAM_API_KEY + '&steamids=' + str(SteamApiUserId)

        SteamApiData = SteamApi.request('GET', SteamApiUrl)
        SteamApiData = SteamApiData.data.decode('utf-8')

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
        ExcelTitle = pd.DataFrame([ExcelTitle])
        ExcelStatsRow = [datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'), 
                        datetime.now().strftime('%H'), datetime.now().strftime('%M'),
                        Player["steamid"], Player["personaname"], Player["personastate"], PlayserStatusText, PlayerGameId, PlayerGameExtraInfo, PlayerGameServerIp]
        ExcelStatsRow = pd.DataFrame([ExcelStatsRow])

        def createExcelFile():
            ExcelTitle.to_excel(str(datetime.now().strftime('%Y_%m_%d_'))+str(SteamApiUserId)+'.xlsx', index=False, header=False)
        def appendExcelStatsRow():
            cur_ExFile = pd.read_excel(str(datetime.now().strftime('%Y_%m_%d_'))+str(SteamApiUserId)+'.xlsx', index_col=None, header=None)
            cur_ExFile = cur_ExFile.append(ExcelStatsRow) 
            cur_ExFile.to_excel(str(datetime.now().strftime('%Y_%m_%d_'))+str(SteamApiUserId)+'.xlsx', index=False, header=False)

        try:
            appendExcelStatsRow()
        except:
            createExcelFile()
            print('New user, Id: ' + str(SteamApiUserId) + ', created a new excel file')
            appendExcelStatsRow()

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + 'Info get SUCCESS, users total: ' + str(len(SteamPlayersToMonitor)))

GetPlayersInfo()

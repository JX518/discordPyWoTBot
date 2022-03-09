import requests
import datetime

# class main:
#     def main():
#         wot = WoTAPI("a5c99768df871fa42a0b10a16e8e89ca")
#         wot.getPlayers()

class WoTAPI:
    def __init__(self, AppID=None):
        if(AppID == None):
            print("No Application ID")
        else:
            print("You set your Application ID as " + AppID)
            self.AppID:str = AppID
            URL = "https://api.worldoftanks.com/wot/account/list/?application_id="+ AppID +"&search=jx5181"
            data = requests.get(url = URL, params = None).json()
            if(data['status'] == "error" and data['status']['error']['field'] == "application_id"):
                raise Exception("Invalid ApplicationID")

    def getID(self, nickname: str) -> str:
        """
            Returns the playerID from a username, if unable to find one, returns None\n

            Arguments:\n
                nickname: \n
                    The string of the account username
        """
        data = self.getPlayers(search = nickname)
        try:
            for player in data['data']:
                if(player['nickname'].lower() == nickname.lower()):
                    ID = player['account_id']
                    return ID
        except KeyError:
            if(len(nickname) < 3):
                raise Exception(nickname + "is too short")
            else:
                raise Exception("No player with the username " + nickname)
        return None

    def getPlayers(self, search: str, fields: str = None, language: str = None, limit: str = None, type: str = None) -> dict:
        """   
        Returns a dictionary of the information from a search\n

        Arguments:\n
            search:\n
            fields: [Optional]\n
                Response field. The fields are separated with commas. Embedded fields are separated \n
                with dots. To exclude a field, use “-” in front of its name. In case the parameter \n
                is not defined, the method returns all fields. Maximum limit: 100.\n
            language: [Optional]\n Localization language
                "en" — English (by default)\n
                "ru" — Русский\n
                "pl" — Polski\n
                "de" — Deutsch\n
                "fr" — Français\n
                "es" — Español\n
                "zh-cn" — 简体中文\n
                "zh-tw" — 繁體中文\n
                "tr" — Türkçe\n
                "cs" — Čeština\n
                "th" — ไทย\n
                "vi" — Tiếng Việt\n
                "ko" — 한국어\n
            limit: [Optional]\n
                The limit to the number of player searches, max at 100\n
            type: [Optional]\n
                startswith" or "exact" search\n
                "startswith" — Search by initial characters of player name. \n
                \tMinimum length: 3 characters. Maximum length: 24 characters. (by default)\n\n
                "exact" — Search by exact match of player name. Case insensitive.\n
                \tYou can enter several names, separated with commas (up to 100).
        """
        URL:str = "https://api.worldoftanks.com/wot/account/list/?application_id=" + self.AppID + "&search=" + search\
        
        if fields != None:  
            URL = URL + "&fields=" + fields
        if(language != None):
            URL = URL + "&language=" + language
        if(limit != None):
            URL = URL + "&limit=" + limit
        if(type != None):
            URL = URL + "&type=" + type

        data = requests.get(url = URL).json()
        return data
    # def serverData() -> dict:
# https://api.worldoftanks.com/wgn/servers/info/?application_id=a5c99768df871fa42a0b10a16e8e89ca&game=wot
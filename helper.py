import requests
import json

def requestSummonerData(summonerName, APIKey):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestTFTSummonerData(summonerName, APIKey): # same as requestSummonerData, they return the same data
    URL = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestTFTRankedData(ID, APIKey):
    URL = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + str(ID) + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestTFTMatchIDS(PUUID, APIKey, count):
    URL = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + str(PUUID) + "/ids" + "?api_key=" + APIKey + "&count=" + str(count)
    response = requests.get(URL)
    return response.json()

def requestMatchData(matchID, APIKey):
    URL = "https://americas.api.riotgames.com/tft/match/v1/matches/" + str(matchID) + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

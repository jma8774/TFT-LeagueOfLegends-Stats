from time import sleep
import matplotlib.pyplot as plt
import requests
import json


def requestSummonerData(summonerName, APIKey):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    while 'status' in response.json() and 'Rate limit' in response.json()['status']['message']:
        print("Rate limit exceeded, trying again in 2 minutes...")
        sleep(121)
        response = requests.get(URL)
        print("Continuing...")
    return response.json()

def requestTFTSummonerData(summonerName, APIKey): # same as requestSummonerData, they return the same data
    URL = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    while 'status' in response.json() and 'Rate limit' in response.json()['status']['message']:
        print("Rate limit exceeded, trying again in 2 minutes...")
        sleep(121)
        response = requests.get(URL)
        print("Continuing...")
    return response.json()

def requestTFTRankedData(ID, APIKey):
    URL = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + str(ID) + "?api_key=" + APIKey
    response = requests.get(URL)
    while 'status' in response.json() and 'Rate limit' in response.json()['status']['message']:
        print("Rate limit exceeded, trying again in 2 minutes...")
        sleep(121)
        response = requests.get(URL)
        print("Continuing...")
    return response.json()

def requestTFTMatchIDS(PUUID, APIKey, count):
    URL = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + str(PUUID) + "/ids" + "?api_key=" + APIKey + "&count=" + str(count)
    response = requests.get(URL)
    while 'status' in response.json() and 'Rate limit' in response.json()['status']['message']:
        print("Rate limit exceeded, trying again in 2 minutes...")
        sleep(121)
        response = requests.get(URL)
        print("Continuing...")
    return response.json()

def requestMatchData(matchID, APIKey):
    URL = "https://americas.api.riotgames.com/tft/match/v1/matches/" + str(matchID) + "?api_key=" + APIKey
    response = requests.get(URL)
    while 'status' in response.json() and 'Rate limit' in response.json()['status']['message']:
        print("Rate limit exceeded, trying again in 2 minutes...")
        sleep(121)
        response = requests.get(URL)
    return response.json()

def plotPie(dataLabelList, title):
    plt.rcParams["font.size"] = 8
    plt.rcParams['font.family'] = "Tahoma"

    labels = [tup[0] for i, tup in enumerate(dataLabelList)]
    data = [tup[1] for i, tup in enumerate(dataLabelList)]
    explode = [0] * len(data)
    print(data)
    m = max(data)
    print(m)
    count = data.count(m)
    print(count)
    if count == 1:
        explode[data.index(m)] = 0.1
    print(explode)
    colors = ['#FF9AA2','#FFB7B2','#FFDAC1','#E2F0CB', '#B5EAD7', '#C7CEEA']
    
    fig1, ax1 = plt.subplots()
    fig1.patch.set_facecolor("#121212")
    patches, out_texts, in_texts = ax1.pie(data, colors = colors, labels=labels, explode=explode, autopct='%0.2f%%', startangle=90, wedgeprops={"edgecolor":"white", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True})
    for out_text in out_texts:
        out_text.set_color('white')
    for in_text in in_texts:
        in_text.set_color('#121212')
        
    ax1.axis('equal') # equal aspect ratio ensures that pie is drawn as a circle
    plt.title(title, color='white', fontsize=11)
    plt.show()
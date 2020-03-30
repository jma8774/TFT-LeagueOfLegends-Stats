from helper import requestSummonerData, requestTFTRankedData, requestTFTMatchIDS, requestMatchData
from time import sleep
from prettytable import PrettyTable
import requests
import json

summonerName = "liliala"
queue_mode = 1090 # 1100 is ranked tft, 1090 is normal tft
APIKey = "RGAPI-731260d9-c48a-48bc-875d-61c2451ec335"

# Summoner Info
summonerData = requestSummonerData(summonerName, APIKey)
print(json.dumps(summonerData, sort_keys=True, indent=1))
ID = summonerData['id']
PUUID = summonerData['puuid']
level = summonerData['summonerLevel']

# Summoner Ranked TFT Info
TFTRankedData = requestTFTRankedData(ID, APIKey)
print(json.dumps(TFTRankedData, sort_keys=True, indent=1))

# Match IDs
numMatches = 200
TFTMatchIDS = requestTFTMatchIDS(PUUID, APIKey, numMatches) # Unfiltered, may contain normal and ranked?

# Each Individual Match's Data
TFTMatchDatas = [] # Filtered to ranked only (queue_id == 1100)
totalPlacement = 0
totalGold = 0
totalTime = 0
traits = {}
units = {}
placements = {}
print("Please wait, receiving information from Riot API...")
for i, value in enumerate(TFTMatchIDS):
    if i % 20 == 0:
        sleep(1.05)
    try:
        matchData = requestMatchData(TFTMatchIDS[i], APIKey)
        if 'metadata' not in matchData:
            print("Rate limit exceeded, have to wait 2 minutes...")
            sleep(121)
            print("Continuing...")
            matchData = requestMatchData(TFTMatchIDS[i], APIKey)

        for j, participants in enumerate(matchData['info']['participants']):
            if matchData['info']['participants'][j]['puuid'] == PUUID and matchData['info']['queue_id'] == queue_mode and matchData['info']['tft_set_number'] == 3:
                totalPlacement += matchData['info']['participants'][j]['placement']
                totalGold += matchData['info']['participants'][j]['gold_left']
                totalTime += matchData['info']['participants'][j]['time_eliminated']
                for k, trait in enumerate(matchData['info']['participants'][j]['traits']): # retriving all traits
                    formatted = trait['name'].replace('Set3_', '')
                    if formatted not in traits:
                        traits[formatted] = 1
                    else:
                        traits[formatted] += 1
                for k, unit in enumerate(matchData['info']['participants'][j]['units']): # retriving all units
                    formatted = unit['character_id'].replace('TFT3_', '')
                    if formatted not in units:
                        units[formatted] = 1
                    else:
                        units[formatted] += 1
                for k, placement in enumerate(matchData['info']['participants'][j]['placement']): # retriving all placements
                    if placement not in placements:
                        placements[placement] = 1
                    else:
                        placements[placement] += 1
                TFTMatchDatas.append(matchData)
                break
    except Exception as err:
        print(err)

# Printing Data
n = len(TFTMatchDatas)
print()
if queue_mode == 1090: # specify whether this is ranked or normal
    print(summonerName.capitalize(), "played", n, "normal games in the last 200 games of set 3 TFT, and in those games they did: (Note that I can only retrieve the most recent 200 games)")
elif queue_mode == 1100:
    print(summonerName.capitalize(), "played", n, "ranked games in the last 200 games of set 3 TFT, and in those games they did: (Note that I can only retrieve the most recent 200 games)")

if n != 0: # check if there are games played
    statsTable = PrettyTable(['Arguments', 'Data'])
    statsTable.add_row(["Average placement", "%0.2f" % (totalPlacement/n)]) # "%0.2f" % str is to format it to 2 decimal places
    statsTable.add_row(["Average gold left", "%0.2f" % (totalGold/n)])
    statsTable.add_row(["Total time spent (minutes)", "%0.2f" % (totalTime/60)])
    print(statsTable)

    traits = sorted(traits.items(), key=lambda x: x[1], reverse=True) # printing all the traits that the summoner went for in a table
    traitsTable = PrettyTable(['Trait', 'Occurrences'])
    for i, value in enumerate(traits):
        traitsTable.add_row([value[0], value[1]])
    print(traitsTable)

    units = sorted(units.items(), key=lambda x: x[1], reverse=True) # printing all the units that the summoner used in a table
    unitsTable = PrettyTable(['Unit Name', 'Occurrences'])
    for i, value in enumerate(units):
        unitsTable.add_row([value[0], value[1]])
    print(unitsTable)

    placements = sorted(placements.items(), key=lambda x: x[1], reverse=True) # printing all the placements that the summoner was placed at
    placementsTable = PrettyTable(['Placement', 'Occurrences'])
    for i, value in enumerate(placements):
        placementsTable.add_row([value[0], value[1]])
    print(placementsTable)
else:
    print("Zero games of the game mode played")
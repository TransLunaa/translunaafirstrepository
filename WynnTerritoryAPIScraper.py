import requests
import json
import time

WynnAPI = requests.get('https://api.wynncraft.com/public_api.php?action=territoryList')

data = WynnAPI.text

parse_json = json.loads(data)

print("----------------------------------------------------------------------------------------")
territory_name = input("Please input the name of the territory: ")
print("----------------------------------------------------------------------------------------")
while True:
    TerritoryOwner = parse_json['territories'][territory_name]['guild']
    GuildPrefix = parse_json['territories'][territory_name]['guildPrefix']
    Acquired = parse_json['territories'][territory_name]['acquired']

    print("You are currently looking at the data of", territory_name)
    print("The guild who currently owns the territory is:", TerritoryOwner, "aka", GuildPrefix)
    print("The guild acquired this territory on", Acquired, "YY/MM/DD")
    print("----------------------------------------------------------------------------------------")

    time.sleep(600)
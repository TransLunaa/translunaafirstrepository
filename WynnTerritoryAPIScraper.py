import requests
import json
import time

guildnamee = input("Please type in the name of the guild you want to view the info of: ")
print("----------------------------------------------------------------------------------------")

WynnAPI = requests.get('https://api.wynncraft.com/public_api.php?action=guildList')

data = WynnAPI.text

parse_json = json.loads(data)

for guildeexists in parse_json["guilds"]:
        guildeeexists = str(guildeexists)
        for guildeeexists in parse_json["guilds"]:
            if guildnamee == guildeeexists:
                print("Succesfully found the guild by the name", guildnamee)
                print("----------------------------------------------------------------------------------------")
                while True:
                    WynnAPI2 = requests.get('https://api.wynncraft.com/public_api.php?action=guildStats&command={}'.format(guildnamee))

                    data2 = WynnAPI2.text

                    parse_json2 = json.loads(data2)

                    GuildName = parse_json2["name"]
                    GuildPrefix = parse_json2["prefix"]
                    xp = parse_json2["xp"]
                    TerritoryNumber = parse_json2["territories"]
                    GuildDateOfCreation = parse_json2["createdFriendly"]

                    xp_left_until_next_level = 100-xp

                    print("The guild you are currently viewing is", GuildName, "aka", GuildPrefix)
                    print(GuildName, "was created on", GuildDateOfCreation)
                    if xp_left_until_next_level <= 20:
                        print(GuildName, "only needs", xp_left_until_next_level, "more percent until the next level")
                    elif xp_left_until_next_level > 20:
                        print(GuildName, "needs", xp_left_until_next_level, "more percent until the next level")
                    print(GuildName, "owns", TerritoryNumber, "territories")
                    print("----------------------------------------------------------------------------------------")
                    print("This text will update in 10 minutes")
                    time.sleep(300)
                    print("----------------------------------------------------------------------------------------")
                    print("This text will update in 5 minutes")
                    print("----------------------------------------------------------------------------------------")
                    time.sleep(300)
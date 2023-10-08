import requests
import json
import time

x = input("Please type the letter  t  if you want to view specific territory api and the letter  g  if you want to view specific guild api: ")
print("Also if you want to view the other api after youve selected one just restart the script")
if x == "t" or x == "T":
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
elif x == "g" or x == "G":
    guildnamee = input("Please type in the name of the guild you want to view the info of: ")
    print("----------------------------------------------------------------------------------------")

    guildexists = 0

    WynnAPI = requests.get("https://api.wynncraft.com/public_api.php?action=guildList")

    data = WynnAPI.text

    parse_json = json.loads(data)

    for guildname in parse_json["guilds"]:
        if guildname == guildnamee:
            print(guildnamee, "exists")
            print("----------------------------------------------------------------------------------------")
            guildexists += 1
        else:
            print("There is no guild by that name sorry")
            quit()

    if guildexists > 0:
        GuildAPI = requests.get("https://api.wynncraft.com/public_api.php?action=guildStats&command={}".format(guildnamee))

        GuildData = GuildAPI.text

        guild_json = json.loads(GuildData)

        ter = guild_json["territories"]
        print(guildnamee, "has", ter, "territories")

        created = guild_json["createdFriendly"]
        print(guildnamee, "was created on", created)

        experience = guild_json["xp"]
        exp = 100-experience
        print(guildnamee, "only needs", exp, "% more xp to level up")
        print("----------------------------------------------------------------------------------------")
        while True:
            ter = guild_json["territories"]
            print(guildnamee, "has", ter, "territories")

            experience = guild_json["xp"]
            exp = 100-experience
            print(guildnamee, "only needs", exp, "% more xp to level up")
            print("----------------------------------------------------------------------------------------")

            time.sleep(600)
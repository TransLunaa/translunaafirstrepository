import requests
import json
import time

debug_flag = 0

def debug(text):
    if (debug_flag == 1):
        print(text)

print("Please type in the letter  t  if you want to view info on territories")
print("or type in the letter  g  to view info on guilds")
x = input()
if x == "g":
    print("---------------------------------------------------------------------------------------------------------")
    guildnamee = "Clear Skies"      # input("Please type in the name of the guild you want to view: ")
    print("---------------------------------------------------------------------------------------------------------")
    WynnAPI = requests.get('https://api.wynncraft.com/public_api.php?action=guildList')

    data = WynnAPI.text

    parse_json = json.loads(data)

    for guildeexists in parse_json["guilds"]:
            guildeeexists = str(guildeexists)
            for guildeeexists in parse_json["guilds"]:
                if guildnamee == guildeeexists:
                    print("Succesfully found the guild by the name", guildnamee)
                    print("---------------------------------------------------------------------------------------------------------")
                    while True:
                        WynnAPI2 = requests.get('https://api.wynncraft.com/public_api.php?action=guildStats&command={}'.format(guildnamee))

                        data2 = WynnAPI2.text

                        parse_json2 = json.loads(data2)

                        GuildName = parse_json2["name"]
                        GuildPrefix = parse_json2["prefix"]
                        xp = parse_json2["xp"]
                        xp_left_until_next_level = 100-xp
                        GuildDateOfCreation = parse_json2["createdFriendly"]
                        
                        # Find the amount of members in a guild and find who is online (the who is online is still in developement)

                        guild_users = []
                        guild_users_length = 0 # only int

                        for memb in parse_json2["members"]:
                            name = memb["name"]
                            guild_users.append(name)
                            guild_users_length += 1

                        WynnAPI3 = requests.get("https://api.wynncraft.com/public_api.php?action=onlinePlayers")

                        debug("data request ok")

                        data3 = WynnAPI3.text

                        parse_json3 = json.loads(data3)
                        debug ("parsed json ok")

                        number_of_guild_members_online = 0

                        for myroot in parse_json3:
                            if (myroot != "request"):
                                # debug("Room: "+myroot)

                                for myuser in parse_json3[myroot]:
                                    if myuser in guild_users:
                                        number_of_guild_members_online += 1
                                        # debug("Guild user online: "+myuser)

                        print(number_of_guild_members_online)

                        # btw a part of the code above this and below the next comment above this one was made with the assistance of chatgpt (not including the "only int")

                        print("The guild you are currently viewing is", GuildName, "aka", GuildPrefix)
                        print("...........................................................")
                        print(GuildName, "was created on", GuildDateOfCreation)
                        if xp_left_until_next_level <= 20:
                            print(GuildName, "only needs", xp_left_until_next_level, "more percent until the next level")
                        elif xp_left_until_next_level > 20:
                            print(GuildName, "needs", xp_left_until_next_level, "more percent until the next level")
                        print("The guild", GuildName, "currently has", guild_users_length, "players in it")
                        print("and of those", guild_users_length, "players there are currently", number_of_guild_members_online, "guild members online")
                        print("---------------------------------------------------------------------------------------------------------")
                        print("This text will update in 15 minutes")
                        time.sleep(300)
                        print("---------------------------------------------------------------------------------------------------------")
                        print("This text will update in 10 minutes")
                        print("---------------------------------------------------------------------------------------------------------")
                        time.sleep(300)
                        print("This text will update in 5 minutes")
                        print("---------------------------------------------------------------------------------------------------------")
                        time.sleep(300)
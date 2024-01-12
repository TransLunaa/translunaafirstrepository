import requests
import json
import time

def space():
    print(" ")
def divider():
    print("-------------------------------------------------------------------------------------------------------")

print("Please type in the letter that corresponds with what you want to see")
divider()
print("g = guild info")
print("f = npc finder")
print("p = player info")
print("n = wynncraft news")
print("w = weapon database")
print("e = exit")
divider()

choice = input()

divider()
if choice == "g" or choice == "G":
    guildnameinput = str(input("Please type in the name of the guild you want to view the info of: "))
    
    guildAPI = requests.get("https://api.wynncraft.com/v3/guild/{}".format(guildnameinput))

    guild_data = guildAPI.text

    parse_json = json.loads(guild_data)

    divider()
        
    print("Succesfully found the guild by the name {}".format(guildnameinput))
    
    divider()

    guildPrefix = parse_json['prefix']
    guildLevel = parse_json['level']
    guildXp = parse_json['xpPercent']
    guildTerritories = parse_json['territories']
    guildWars = parse_json['wars']

    # Finds the date of when the guild was created and makes it more understandable
    arr = []
    arr2 = []
    for date in parse_json['created']:
        arr.append(date)
    x = 0
    for i in range(10):
        arr2.append(arr[x])
        x += 1
    easydate = ''.join(arr2)
    
    
    # Finds the names of players online from the guild (btw ty dad for helping me code this part) and start of loop
    while True:
        guildAPI = requests.get("https://api.wynncraft.com/v3/guild/{}".format(guildnameinput))

        guild_data = guildAPI.text

        parse_json = json.loads(guild_data)

        memberList = []
        memberOnlineList = []
        memberNum = 0
        memberOnlineNum = 0
        for names in parse_json['members']:        
            if (names != "total"):
                for member_name in parse_json['members'][names]:
                    memberList.append(member_name)
                    memberNum += 1

        playerListAPI = requests.get("https://api.wynncraft.com/v3/player")

        playerListData = playerListAPI.text

        parse_json2 = json.loads(playerListData)

        for myroot in parse_json2:
            for myuser in parse_json2['players']:
                if myuser in memberList:
                    memberOnlineList.append(myuser)
        memberOnlineList = list(dict.fromkeys(memberOnlineList))
        memberOnlineNum = len(memberOnlineList)
        
        print("The guild you are currently looking at is", guildnameinput, "aka", guildPrefix)
        print("The guild was created on", easydate)
        if guildXp < 80:
            print("The guild is currently at level", guildLevel, "and needs", 100-guildXp, "more percent to level up")
        else:
            print("The guild is currently at level", guildLevel, "and only needs", 100-guildXp, "more percent to level up")
        print("The guild has warred", guildWars, "times and currently owns", guildTerritories, "territories")
        print("The guild currently has", memberNum, "members and of those", memberNum, "members there are currently", memberOnlineNum, "online")
        if memberOnlineNum > 0:
            print("and those", memberOnlineNum, "online members are:", memberOnlineList)
        divider()
        print("This text will update in 10 minutes")
        time.sleep(300)
        print("This text will update in 5 minutes")
        divider()
        time.sleep(300)
elif choice == "f" or choice == "F":
    NPCLocationAPI = requests.get("https://api.wynncraft.com/v3/map/locations/markers")

    NPCLocationData = NPCLocationAPI.text

    parse_json3 = json.loads(NPCLocationData)

    coordinates_full_list = []
    x_coordinates = []
    y_coordinates = []
    z_coordinates = []
    xyz_coordinates = []

    NPCType = input("Please type in the name of the npc you want to view the locations of: ")
    divider()
    for npcstr in parse_json3:
        if npcstr['name'] == "{}".format(NPCType):
            x_coordinates_ = npcstr['x']
            x_coordinates.append(x_coordinates_)
            xyz_coordinates.append(x_coordinates)
            x_coordinates = []
            y_coordinates_ = npcstr['y']
            y_coordinates.append(y_coordinates_)
            xyz_coordinates.append(y_coordinates)
            y_coordinates = []
            z_coordinates_ = npcstr['z']
            z_coordinates.append(z_coordinates_)
            xyz_coordinates.append(z_coordinates)
            z_coordinates = []
            strxyz_coordinates = str(xyz_coordinates)
            strxyz_coordinates = strxyz_coordinates.replace('[', '')
            strxyz_coordinates = strxyz_coordinates.replace(']', '')
            strxyz_coordinates = strxyz_coordinates.replace("'", '')
            strxyz_coordinates = strxyz_coordinates.replace(',', '')
            print("Found a {} at these coordinates: {}".format(NPCType, strxyz_coordinates))
            xyz_coordinates = []
    divider()

    time.sleep(600)
elif choice == "p" or choice == "P":
    playerName = input("Please input the name of the player you want to view info about: ")
    divider()
    
    playerAPI = requests.get("https://api.wynncraft.com/v3/player/{}".format(playerName))

    playerData = playerAPI.text

    parse_json4 = json.loads(playerData)

    if parse_json4['publicProfile'] == True:

        if parse_json4['online'] == True:
            print("{} is currently online in world {}".format(playerName, parse_json4['server']))
        else:
            print("{} is currently offline".format(playerName))

        print("{} has {} hours played in total".format(playerName, parse_json4['playtime']))

        if parse_json4['guild'] != None:
            print("{} are apart of the guild {} and have the rank {}".format(playerName, parse_json4['guild']['name'], str(parse_json4['guild']['rank']).capitalize()))
        else:
            pass
        
        if parse_json4['supportRank'] != None:
            print("{} has the {} support rank".format(playerName, parse_json4['supportRank']))
        else:
            print("{} does not own a support rank".format(playerName))

        print("{} have been in {} wars".format(playerName, parse_json4['globalData']['wars']))

        print("{} has completed {} dungeons and {} raids".format(playerName, parse_json4['globalData']['dungeons']['total'], parse_json4['globalData']['raids']['total']))

        time.sleep(600)
    else:
        print("Sorry, the player you are looking for does not have a public profile")
        time.sleep(3)
elif choice == "n" or choice == "N":
    newsAPI = requests.get("https://api.wynncraft.com/v3/latest-news")

    newsData = newsAPI.text

    parse_json5 = json.loads(newsData)

    print("Please type in a letter that corresponds with a category you want to search")
    divider()
    print("d = news posted on certain dates")
    print("p = poster of the news article")
    print("n = name of the article")
    print("e = exit")
    divider()

    choice2 = input()
    divider()

    if choice2 == "d" or choice2 == "D":
        newsDate = input("Please type in a day of the month or name of the month or number of the year you want to search for: ")
        divider()
        for news in parse_json5:
            if newsDate in news['date']:
                print(news['forumThread'])
    elif choice2 == "p" or choice2 == "P":
        newsPoster = input("Pleast type in the name of someone who you want to see the articles from: ")
        divider()
        for news in parse_json5:
            if newsPoster in news['author']:
                print(news['forumThread'])
    elif choice2 == "n" or choice2 == "N":
        newsKeywords = input("Please type in a keyword to search articles that contain that word: ")
        divider()
        for news in parse_json5:
            if newsKeywords in news['title']:
                print(news['forumThread'])

    elif choice2 == "e" or choice2 == "E":
        quit()
    else:
        print("Sorry, what you wrote is not associated with any category, please try again")
        time.sleep(3)
        quit()

    time.sleep(600)
elif choice == "w" or choice == "W":
    weaponName = input("Please type in the name of the weapon you want to view the info of: ")

    divider()

    weaponAPI = requests.get("https://api.wynncraft.com/v3/item/search/{}".format(weaponName))

    weaponData = weaponAPI.text

    parse_json6 = json.loads(weaponData)

    print("{} is a {} {} with {} attack speed and requires you to have combat level {}".format(weaponName, parse_json6[weaponName]['tier'].capitalize(), parse_json6[weaponName]['type'].capitalize(), parse_json6[weaponName]['attackSpeed'].replace('_', ' '), parse_json6[weaponName]['requirements']['level']))
    print("{}'s average DPS is {}".format(weaponName, parse_json6[weaponName]['base']['averageDPS']))

    time.sleep(600)
elif choice == "e" or choice == "E":
    quit()
else:
    print("Sorry, what you wrote is not associated with any category, please try again")
    time.sleep(3)
    quit()
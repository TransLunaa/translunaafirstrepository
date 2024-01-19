import requests
import json
import time

def divider():
    print("-------------------------------------------------------------------------------------------------------")

print("Please type in the letter that corresponds with what you want to see")
divider()
print("g = guild info")
print("f = npc finder")
print("p = player info")
print("n = wynncraft news")
print("i = item database")
print("t = territory info")
print("e = exit")
divider()

choice = input()

divider()
if choice == "g" or choice == "G":
    guildnameinput = str(input("Please type in the name or prefix of the guild you want to view the info of: "))
    
    if len(guildnameinput) > 4:
        guildAPI = requests.get("https://api.wynncraft.com/v3/guild/{}".format(guildnameinput))
    elif len(guildnameinput) <= 4:
        guildAPI = requests.get("https://api.wynncraft.com/v3/guild/prefix/{}".format(guildnameinput.capitalize()))

    guild_data = guildAPI.text

    parse_json = json.loads(guild_data)

    divider()
    
    if "Error" not in parse_json:
        print("Succesfully found the guild by the name {}".format(guildnameinput))
    else:
        print("Sorry but there doesnt seem to be a guild by the name {}, please try again once the program closes itself".format(guildnameinput))
        time.sleep(3)
        quit()
    
    divider()

    if len(guildnameinput) > 4:
        guildPrefixOrName = parse_json['prefix']
    elif len(guildnameinput) <= 4:
        guildPrefixOrName = parse_json['name']
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
        if len(guildnameinput) > 4:
            guildAPI = requests.get("https://api.wynncraft.com/v3/guild/{}".format(guildnameinput))
        elif len(guildnameinput) <= 4:
            guildAPI = requests.get("https://api.wynncraft.com/v3/guild/prefix/{}".format(guildnameinput.capitalize()))

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
        
        if len(guildnameinput) > 4:
            print("The guild you are currently looking at is", guildnameinput, "aka", guildPrefixOrName)
        elif len(guildnameinput) <= 4:
            print("The guild you are currently looking at is", guildPrefixOrName, "aka", guildnameinput)
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

    if parse_json4['online'] == True:
        print("{} is currently online in world {}".format(playerName, parse_json4['server']))
    else:
        print("{} is currently offline".format(playerName))

    print("{} has {} hours played in total".format(playerName, parse_json4['playtime']))

    if parse_json4['guild'] != None:
            print("{} is apart of the guild {} and has the rank {}".format(playerName, parse_json4['guild']['name'], str(parse_json4['guild']['rank']).capitalize()))
    else:
        pass
        
    if parse_json4['supportRank'] != None:
        print("{} has the {} support rank".format(playerName, parse_json4['supportRank']))
    else:
        print("{} does not own a support rank".format(playerName))

    print("{} has been in {} wars".format(playerName, parse_json4['globalData']['wars']))

    print("{} has completed {} dungeons and {} raids".format(playerName, parse_json4['globalData']['dungeons']['total'], parse_json4['globalData']['raids']['total']))

    time.sleep(600)
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
        print("Sorry, what you wrote is not associated with any category, please try again once the program closes itself")
        time.sleep(3)
        quit()

    time.sleep(600)
elif choice == "i" or choice == "I":
    itemName = input("Please type in the name of the item you want to view the info of: ")

    divider()

    itemAPI = requests.get("https://api.wynncraft.com/v3/item/search/{}".format(itemName))

    itemData = itemAPI.text

    parse_json6 = json.loads(itemData)

    allWeaponTypes = ['dagger', 'wand', 'bow', 'spear', 'relik']
    allArmorTypes = ['helmet', 'chestplate', 'leggings', 'boots']
    allAccessoryTypes = ['ring', 'bracelet', 'necklace']
    allCharms = ['Charm of the Stone', 'Charm of the Light', 'Charm of the Void', 'Charm of the Worm']

    def itemRequirementsStatsAndIdentifications():
        divider()
        if "base" in parse_json6[itemName]:
            print("{}'s stats are:".format(itemName))
            for itemStats in parse_json6[itemName]['base']:
                print(itemStats)
                divider()
        allRequirements = []
        for allItemRequirements in parse_json6[itemName]['requirements']:
            if allItemRequirements != "level":
                allRequirements.append(allItemRequirements)
        if allRequirements != []:
            print("{}'s requirements are:".format(itemName))
            for itemRequirements in parse_json6[itemName]['requirements']:
                if itemRequirements != "level":
                    print(itemRequirements)
            divider()
        if "identifications" in parse_json6[itemName]:
            print("{}'s bonus stats are:".format(itemName))
            for itemIdentifications in parse_json6[itemName]['identifications']:
                print(" ")
                print(itemIdentifications)

    if parse_json6[itemName]['internalName'] in allCharms:
        print("{} is a {} charm you obtain from the raid {}, and {} requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['dropMeta']['name'], itemName, parse_json6[itemName]['requirements']['level']))
        divider()
        if "identifications" in parse_json6[itemName]:
            print("{}'s bonus stats are:".format(itemName))
            for itemIdentifications in parse_json6[itemName]['identifications']:
                print(" ")
                print(itemIdentifications)
    elif "type" in parse_json6[itemName]:
        if parse_json6[itemName]['type'] in allWeaponTypes:
            print("{} is a {} {} with {} attack speed, {} powder slots and requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'].capitalize(), parse_json6[itemName]['type'].capitalize(), parse_json6[itemName]['attackSpeed'].replace('_', ' '), parse_json6[itemName]['powderSlots'], parse_json6[itemName]['requirements']['level']))
            allWeaponRequirements = ['strength', 'dexterity', 'intelligence', 'agility', 'defence']
            itemAllRequirements = []
            for requirement in parse_json6[itemName]['requirements']:
                if requirement != "level":
                    itemAllRequirements.append(requirement)
            if itemAllRequirements != []:
                print("and also these requirements:")
                for itemRequirements in parse_json6[itemName]['requirements']:
                        if itemRequirements != "level":
                            print("{}: {}".format(itemRequirements.capitalize(), parse_json6[itemName]['requirements'][itemRequirements]))
            divider()
            print("{}'s average DPS is {}".format(itemName, parse_json6[itemName]['base']['averageDPS']))
            if "base" in parse_json6[itemName]:
                allDmgTypes = ['fireDamage', 'waterDamage', 'airDamage', 'thunderDamage', 'earthDamage']
                itemAllDamageTypes = []
                for itemDamageTypes in parse_json6[itemName]['base']:
                    if itemDamageTypes != "averageDPS" and itemDamageTypes != "damage":
                        itemAllDamageTypes.append(itemDamageTypes)
                if itemAllDamageTypes != []:
                    print("{} has these damage types:".format(itemName))
                    if itemAllDamageTypes == allDmgTypes:
                        print("{} has rainbow damage".format(itemName))
                    else:
                        print(itemAllDamageTypes)
            if "identifications" in parse_json6[itemName]:
                divider()
                print("{}'s bonus stats are:".format(itemName))
                for itemIdentifications in parse_json6[itemName]['identifications']:
                    print(" ")
                    print(itemIdentifications)
            if "lore" in parse_json6[itemName]:
                divider()
                print("{}'s lore says: {}".format(itemName, parse_json6[itemName]['lore']))
        elif parse_json6[itemName]['type'] in allArmorTypes:
            if parse_json6[itemName]['type'] == "boots" or parse_json6[itemName]['type'] == "leggings":
                print("{} is a pair of {} {} that requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['type'], parse_json6[itemName]['requirements']['level']))
            else:
                print("{} is a {} {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['type']))
            divider()
            if "base" in parse_json6[itemName]:
                print("{}'s stats are:".format(itemName))
                for itemStats in parse_json6[itemName]['base']:
                    print("{}: {}".format(itemStats, parse_json6[itemName]['base'][itemStats]))
                divider()
            allRequirements = []
            for allItemRequirements in parse_json6[itemName]['requirements']:
                if allItemRequirements != "level":
                    allRequirements.append(allItemRequirements)
            if allRequirements != []:
                print("{}'s other requirements are:".format(itemName))
                for itemRequirements in parse_json6[itemName]['requirements']:
                    if itemRequirements != "level":
                        print("{}: {}".format(itemRequirements.capitalize(), parse_json6[itemName]['requirements'][itemRequirements]))
            if "identifications" in parse_json6[itemName]:
                divider()
                print("{}'s bonus stats are:".format(itemName))
                for itemIdentifications in parse_json6[itemName]['identifications']:
                    print(" ")
                    print(itemIdentifications)
            if "lore" in parse_json6[itemName]:
                divider()
                print("{}'s lore says: {}".format(itemName, parse_json6[itemName]['lore']))
        elif parse_json6[itemName]['type'] in allAccessoryTypes:
            print("{} is a {} {} that requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['accessoryType'], parse_json6[itemName]['requirements']['level']))
            divider()
            if "base" in parse_json6[itemName]:
                print("{}'s stats are:".format(itemName))
                for itemStats in parse_json6[itemName]['base']:
                    print(itemStats)
                    divider()
            allRequirements = []
            for allItemRequirements in parse_json6[itemName]['requirements']:
                if allItemRequirements != "level":
                    allRequirements.append(allItemRequirements)
            if allRequirements != []:
                print("{}'s requirements are:".format(itemName))
                for itemRequirements in parse_json6[itemName]['requirements']:
                    if itemRequirements != "level":
                        print(itemRequirements)
                divider()
            if "identifications" in parse_json6[itemName]:
                print("{}'s bonus stats are:".format(itemName))
                for itemIdentifications in parse_json6[itemName]['identifications']:
                    print(" ")
                    print(itemIdentifications)
                divider()
            if "lore" in parse_json6[itemName]:
                divider()
                print("{}'s lore says: {}".format(itemName, parse_json6[itemName]['lore']))
    elif "tomeType" in parse_json6[itemName]:
        if parse_json6[itemName]['raidReward'] == False:
            print("{} is a {} tome that requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['requirements']['level']))
        else:
            print("{} is a {} tome that requires you to have atleast combat level {} and that you can obtain from {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['requirements']['level'], parse_json6[itemName]['dropMeta']['name']))
        itemRequirementsStatsAndIdentifications()
    elif "ingredientPositionModifiers" in parse_json6[itemName]:
        print("{} is a tier {} material".format(itemName, parse_json6[itemName]['tier']))
        print("that is dropped by:")
        for mobThatDropsItem in parse_json6[itemName]['droppedBy']:
            print(mobThatDropsItem)
        divider()
        print("{} requires you to have atleast level {} in:".format(itemName, parse_json6[itemName]['requirements']['level']))
        for skillRequirement in parse_json6[itemName]['requirements']['skills']:
            print(skillRequirement.capitalize())
        divider()
        if parse_json6[itemName]['itemOnlyIDs']['durabilityModifier'] < 0:
            print("{} decreases the durability of an item by {}".format(itemName, parse_json6[itemName]['itemOnlyIDs']['durabilityModifier']))
        elif parse_json6[itemName]['itemOnlyIDs']['durabilityModifier'] > 0:
            print("{} increases the durability of an item by {}".format(itemName, parse_json6[itemName]['itemOnlyIDs']['durabilityModifier']))
        else:
            print("{} doesnt change the durability of an item".format(itemName))
        divider()
        if parse_json6[itemName]['consumableOnlyIDs']['duration'] < 0:
            print("{} decreases the duration of an item by {}".format(itemName, parse_json6[itemName]['consumableOnlyIDs']['duration']))
        elif parse_json6[itemName]['consumableOnlyIDs']['durabilityModifier'] > 0:
            print("{} increases the duration of an item by {}".format(itemName, parse_json6[itemName]['consumableOnlyIDs']['duration']))
        else:
            print("{} doesnt change the duration of an item".format(itemName))
        divider()
        if parse_json6[itemName]['consumableOnlyIDs']['charges'] < 0:
            print("{} decreases the charges of an item by {}".format(itemName, parse_json6[itemName]['consumableOnlyIDs']['charges']))
        elif parse_json6[itemName]['consumableOnlyIDs']['charges'] > 0:
            print("{} increases the charges of an item by {}".format(itemName, parse_json6[itemName]['consumableOnlyIDs']['charges']))
        else:
            print("{} doesnt change the charges of an item".format(itemName))
        divider()
        print("the item {} creates have these requirements added to:".format(itemName))
        for skillRequirements in parse_json6[itemName]['itemOnlyIDs']:
            if skillRequirements != "durabilityModifier":
                if skillRequirements != 0:
                    print("{}: {}".format(skillRequirements, parse_json6[itemName]['itemOnlyIDs'][skillRequirements]))
        positionModifiers = []
        for ingredientPositions in parse_json6[itemName]['ingredientPositionModifiers']:
            if ingredientPositions != 0:
                positionModifiers.append(ingredientPositions)
        if positionModifiers != []:
            divider()
            print("{} also has these position modifiers:".format(itemName))
            for itemPositionModifiers in parse_json6[itemName]['ingredientPositionModifiers']:
                if itemPositionModifiers != 0:
                    print("{}: {}".format(itemPositionModifiers, parse_json6[itemName]['ingredientPositionModifiers'][itemPositionModifiers]))
    elif "craftable" in parse_json6[itemName]:
        print("{} is a tier 2 resource that requires you to have atleast {} level {}, and you can use it to make:".format(itemName, parse_json6[itemName]['requirements']['skills'], parse_json6[itemName]['requirements']['level']))
        for craftableItems in parse_json6[itemName]['craftable']:
            print(craftableItems.capitalize())
    time.sleep(600)
elif choice == "t" or choice == "T":
    territoryAPI = requests.get("https://api.wynncraft.com/v3/guild/list/territory")

    territoryData = territoryAPI.text

    parse_json7 = json.loads(territoryData)

    print("Please type in a letter that corresponds with what you want to view: ")
    divider()
    print("w = what guild owns what")
    print("i = info on a specific territory")
    print("e = exit")
    divider()

    choice3 = input()
    divider()

    if choice3 == "w" or choice3 == "W":
        territoryGuildName = []

        for territory in parse_json7:
            territoryGuildName.append(parse_json7[territory]['guild']['name'])
        territoryGuildNames = []
        guildNum = []
        for duplicates in territoryGuildName:
            n = territoryGuildName.count(duplicates)
            if n > 1:
                if territoryGuildNames.count(duplicates) == 0:
                    territoryGuildNames.append(duplicates)
                    guildNum.append(n)
        n = 0
        while n < len(territoryGuildNames):
            print("The guild", territoryGuildNames[n], "owns", guildNum[n], "territories")
            n += 1
    elif choice3 == "i" or choice3 == "I":
        territoryName = input("Please type in the name of the territory you want to view info about: ")
        divider()

        if territoryName in parse_json7:
            print("Succesfully found a territory by the name {}".format(territoryName))
            divider()
        else:
            print("Sorry but there doesnt seem to be a territory called {}, please try again once the program closes itself".format(territoryName))
            time.sleep(3)
            quit()

        arr = []
        arr2 = []
        for date in parse_json7[territoryName]['acquired']:
            arr.append(date)
        x = 0
        for i in range(10):
            arr2.append(arr[x])
            x += 1
        easydate = ''.join(arr2)

        startX = abs(parse_json7[territoryName]['location']['start'][0])
        startZ = abs(parse_json7[territoryName]['location']['start'][1])
        endX = abs(parse_json7[territoryName]['location']['end'][0])
        endZ = abs(parse_json7[territoryName]['location']['end'][1])

        if startX > endX:
            sideX = startX-endX
        else:
            sideX = endX-startX
        if startZ > endZ:
            sideZ = startZ-endZ
        else:
            sideZ = endZ-startZ
        territoryArea = sideX*sideZ

        print("{}'s area is {} blocks squared".format(territoryName, territoryArea))
        print("{}'s bottom-left corner is at {} {} (x, z)".format(territoryName, startX, startZ))
        print("{}'s top-left corner is at {} {} (x, z)".format(territoryName, startX, endZ))
        print("{}'s top-right corner is at {} {} (x, z)".format(territoryName, endX, endZ))
        print("{}'s bottom-right corner is at {} {} (x, z)".format(territoryName, endX, startZ))
        divider()
        while True:
            print("The owner of the territory you are currently looking at ({}) is {} aka {} and they acquired the territory on {}".format(territoryName, parse_json7[territoryName]['guild']['name'], parse_json7[territoryName]['guild']['prefix'], easydate))
            divider()
            print("This text will update in 10 minutes")
            divider()
            time.sleep(300)
            print("This text will update in 5 minutes")
            divider()
            time.sleep(300)
    elif choice3 == "e" or choice3 == "E":
        quit()
    else:
        print("Sorry, what you wrote is not associated with any category, please try again once the program closes itself")
        time.sleep(3)
        quit()

    time.sleep(600)
elif choice == "e" or choice == "E":
    quit()
else:
    print("Sorry, what you wrote is not associated with any category, please try again once the program closes itself")
    time.sleep(3)
    quit()
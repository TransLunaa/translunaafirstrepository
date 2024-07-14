import requests
import json
import time
import os
import string

def divider():
    print("---------------------------------------------------------------------------------------------------------------------")

wynncraftAPI = "https://api.wynncraft.com/v3/"

while True:
    print("Please type in a letter that corresponds with what you want to see")
    divider()
    print("g = guild info")
    print("f = npc finder")
    print("p = player info")
    print("n = wynncraft news")
    print("i = item database")
    print("t = territory info")
    print("c = clear everything in the terminal")
    print("e = exit")
    divider()

    choice = input()

    divider()
    if choice.lower() == "g":
        # Guild info
        guildnameinput = str(input("Please type in the name or prefix of the guild you want to view the info of: "))
        
        if len(guildnameinput) > 4:
            guildAPI = requests.get("{}guild/{}".format(wynncraftAPI, guildnameinput))
        elif len(guildnameinput) <= 4:
            guildAPI = requests.get("{}guild/prefix/{}".format(wynncraftAPI, guildnameinput.capitalize()))

        guild_data = guildAPI.text

        parse_json = json.loads(guild_data)

        divider()
        
        if "Error" not in parse_json:
            print("Succesfully found the guild by the name {}".format(guildnameinput))
        else:
            print("Sorry but there doesnt seem to be a guild by the name {}, please try again once the program restarts itself".format(guildnameinput))
            time.sleep(3)
            divider()
            continue
        
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
        x = 0
        for i in range(len(arr2)):
            if arr2[x] == "-":
                arr2.pop(x)
            else:
                x += 1
        easyDates = []
        x = 0
        while x <= 3:
            easyDates.append(arr2[x])
            x += 1
        easyDate1 = ''.join(easyDates)
        easyDates.clear()
        while x >= 4 and x <= 5:
            easyDates.append(arr2[x])
            x += 1
        easyDate2 = ''.join(easyDates)
        easyDates.clear()
        while x >= 6 and x <= 7:
            easyDates.append(arr2[x])
            x += 1
        x = 0
        if easyDates[1] == "1":
            x = 1
        elif easyDates[1] == "2":
            x = 2
        elif easyDates[1] == "3":
            x = 3
        else:
            x = 4
        easyDate3 = ''.join(easyDates)
        easyDates.clear()
        monthsDict = {
            "01": 'January',
            "02": 'February',
            "03": 'March',
            "04": 'April',
            "05": 'May',
            "06": 'June',
            "07": 'July',
            "08": 'August',
            "09": 'September',
            "10": 'October',
            "11": 'November',
            "12": 'December'
        }
        easyDate3 = int(easyDate3)
        
        # Finds the names of players online from the guild (btw ty dad for helping me code this part) and start of loop
        while True:
            if len(guildnameinput) > 4:
                guildAPI = requests.get("{}guild/{}".format(wynncraftAPI, guildnameinput))
            elif len(guildnameinput) <= 4:
                guildAPI = requests.get("{}guild/prefix/{}".format(wynncraftAPI, guildnameinput.capitalize()))

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

            playerListAPI = requests.get("{}player".format(wynncraftAPI))

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
            if x == 1:
                print(f"The guild was created on the {easyDate3}st of {monthsDict[easyDate2]} {easyDate1}")
            elif x == 2:
                print(f"The guild was created on the {easyDate3}nd of {monthsDict[easyDate2]} {easyDate1}")
            elif x == 3:
                print(f"The guild was created on the {easyDate3}rd of {monthsDict[easyDate2]} {easyDate1}")
            else:
                print(f"The guild was created on the {easyDate3}th of {monthsDict[easyDate2]} {easyDate1}")
            if guildXp < 80:
                print("The guild is currently at level", guildLevel, "and needs", 100-guildXp, "more percent to level up")
            else:
                print("The guild is currently at level", guildLevel, "and only needs", 100-guildXp, "more percent to level up")
            print("The guild has warred", guildWars, "times and currently owns", guildTerritories, "territories")
            print("The guild currently has", memberNum, "members and of those", memberNum, "members there are currently", memberOnlineNum, "online")
            if memberOnlineNum > 0:
                print("and those", memberOnlineNum, "online members are:", memberOnlineList)
            divider()
            break
            
    elif choice.lower() == "f":
        # NPC location info
        NPCLocationAPI = requests.get("{}map/locations/markers".format(wynncraftAPI))

        NPCLocationData = NPCLocationAPI.text

        parse_json3 = json.loads(NPCLocationData)

        coordinates_full_list = []
        x_coordinates = []
        y_coordinates = []
        z_coordinates = []
        xyz_coordinates = []

        NPCType = input("Please type in the name of the npc you want to view the locations of: ")

        if NPCType in parse_json3:
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
        else:
            divider()
            print("Sorry the name of the npc you typed in doesnt exist please try again once the program restarts itself")
            divider()

    elif choice.lower() == "p":
        # player info
        playerName = input("Please input the name of the player you want to view info about: ")
        divider()
        
        playerAPI = requests.get("{}player/{}".format(wynncraftAPI, playerName))

        playerData = playerAPI.text

        parse_json4 = json.loads(playerData)

        try:
            if parse_json4['Error'] != None:
                print("The player youre trying to find has either changed their username or hasnt played on wynn yet, please try again")
                divider()
                continue
        except KeyError:
            pass
        
        arr = []
        arr2 = []
        for date in parse_json4['firstJoin']:
            arr.append(date)
        x = 0
        for i in range(10):
            arr2.append(arr[x])
            x += 1
        x = 0
        for i in range(len(arr2)):
            if arr2[x] == "-":
                arr2.pop(x)
            else:
                x += 1
        easyDates = []
        x = 0
        while x <= 3:
            easyDates.append(arr2[x])
            x += 1
        easyDate1 = ''.join(easyDates)
        easyDates.clear()
        while x >= 4 and x <= 5:
            easyDates.append(arr2[x])
            x += 1
        easyDate2 = ''.join(easyDates)
        easyDates.clear()
        while x >= 6 and x <= 7:
            easyDates.append(arr2[x])
            x += 1
        x = 0
        if easyDates[1] == "1":
            x = 1
        elif easyDates[1] == "2":
            x = 2
        elif easyDates[1] == "3":
            x = 3
        else:
            x = 4
        easyDate3 = ''.join(easyDates)
        easyDates.clear()
        monthsDict = {
            "01": 'January',
            "02": 'February',
            "03": 'March',
            "04": 'April',
            "05": 'May',
            "06": 'June',
            "07": 'July',
            "08": 'August',
            "09": 'September',
            "10": 'October',
            "11": 'November',
            "12": 'December'
        }
        easyDate3 = int(easyDate3)

        if x == 1:
            print(f"{playerName} first joined on the {easyDate3}st of {monthsDict[easyDate2]} {easyDate1}")
        elif x == 2:
            print(f"{playerName} first joined on the {easyDate3}nd of {monthsDict[easyDate2]} {easyDate1}")
        elif x == 3:
            print(f"{playerName} first joined on the {easyDate3}rd of {monthsDict[easyDate2]} {easyDate1}")
        else:
            print(f"{playerName} first joined on the {easyDate3}th of {monthsDict[easyDate2]} {easyDate1}")

        if parse_json4['online'] == True:
            print("{} is currently online in world {}".format(playerName, parse_json4['server']))
        else:
            print("{} is currently offline".format(playerName))

        print("{} has {} hours played in total".format(playerName, parse_json4['playtime']))

        if parse_json4['guild'] != None:
                print("{} is apart of the guild {} ({}) and has the rank {}".format(playerName, parse_json4['guild']['name'], parse_json4['guild']['prefix'], str(parse_json4['guild']['rank']).capitalize()))

        if parse_json4['supportRank'] != None:
            print("{} has the {} support rank".format(playerName, parse_json4['supportRank']))
        else:
            print("{} does not own a support rank".format(playerName))

        if parse_json4['globalData']['wars'] > 0:
            print("{} has been in {} wars".format(playerName, parse_json4['globalData']['wars']))

        print("{} has completed {} dungeons and {} raids".format(playerName, parse_json4['globalData']['dungeons']['total'], parse_json4['globalData']['raids']['total']))
        divider()
        dungeonsAndRaidsChoice = input("Do you want to view more info on raids/dungeons? (please type in the letter y if yes): ")
        divider()
        if dungeonsAndRaidsChoice.lower() == "y":
            print("From the {} dungeons and {} raids {} has completed:".format(parse_json4['globalData']['raids']['total'], parse_json4['globalData']['dungeons']['total'], playerName))
            divider()
            dungeonsList = []
            dungeonsAndRaidsNum = 0
            for dungeons in parse_json4['globalData']['dungeons']['list']:
                dungeonsList.append(dungeons)
            for i in range(len(dungeonsList)):
                print("{} of the dungeons completed in total is the {} dungeon".format(parse_json4['globalData']['dungeons']['list'][dungeonsList[dungeonsAndRaidsNum]], dungeonsList[dungeonsAndRaidsNum]))
                dungeonsAndRaidsNum += 1
            if parse_json4['globalData']['raids']['total'] > 0:
                print(" ")
            raidList = []
            for raids in parse_json4['globalData']['raids']['list']:
                raidList.append(raids)
            dungeonsAndRaidsNum = 0
            for i in range(len(raidList)):
                print("{} of the raids completed in total is {}".format(parse_json4['globalData']['raids']['list'][raidList[dungeonsAndRaidsNum]], raidList[dungeonsAndRaidsNum]))
                dungeonsAndRaidsNum += 1
            divider()
    elif choice.lower() == "n":
        # news info
        newsAPI = requests.get("{}latest-news".format(wynncraftAPI))

        newsData = newsAPI.text

        parse_json5 = json.loads(newsData)

        print("Please type in a letter that corresponds with a category you want to search")
        divider()
        print("a = all articles")
        print("e = exit")
        divider()

        choice2 = input()

        if choice2.lower() == "a":
            for news in parse_json5:
                divider()
                print("The link to the article called {} by {} is:".format(news['title'], news['author']))
                print(" ")
                print(news['forumThread'])
        elif choice2.lower() == "e":
            continue
        else:
            print("Sorry, what you wrote is not associated with any category, please try again once the program restarts itself")
            time.sleep(3)
            divider()
            continue
            
        divider()
    elif choice.lower() == "i":
        # item database info
        itemName = input("Please type in the name of the item you want to view the info of: ")

        divider()

        itemAPI = requests.get("{}item/search/{}".format(wynncraftAPI, itemName))

        itemData = itemAPI.text

        parse_json6 = json.loads(itemData)

        allWeaponTypes = ['dagger', 'wand', 'bow', 'spear', 'relik']
        allArmorTypes = ['helmet', 'chestplate', 'leggings', 'boots']
        allAccessoryTypes = ['ring', 'bracelet', 'necklace']
        allCharms = ['Charm of the Stone', 'Charm of the Light', 'Charm of the Void', 'Charm of the Worm']
        allRawStats = ['rawDefence', 'rawStrength', 'rawIntelligence', 'rawAgility', 'rawDexterity']

        # defines the function for tomes
        def itemRequirementsStatsAndIdentifications():
            divider()
            if "averageDPS" in parse_json6[itemName]['base']:
                print("{}'s base average DPS is {}".format(itemName, parse_json6[itemName]['base']['averageDPS']))
                divider()
            if "base" in parse_json6[itemName]:
                print("{}'s stats are:".format(itemName))
                print(" ")
                for itemStats in parse_json6[itemName]['base']:
                    print(itemStats)
                    divider()
            allRequirements = []
            for allItemRequirements in parse_json6[itemName]['requirements']:
                if allItemRequirements != "level":
                    allRequirements.append(allItemRequirements)
            if allRequirements != []:
                print("{}'s requirements are:".format(itemName))
                print(" ")
                for itemRequirements in parse_json6[itemName]['requirements']:
                    if itemRequirements != "level":
                        print(itemRequirements)
            if "identifications" in parse_json6[itemName]:
                print("{}'s bonus stats are:".format(itemName))
                for itemIdentifications in parse_json6[itemName]['identifications']:
                    print(" ")
                    if itemIdentifications == "xpBonus":
                        print("{}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                    else:
                        print("Bonus {}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                print(" ")
            if "lore" in parse_json6[itemName]:
                divider()
                print("{}'s lore says: {}".format(itemName, parse_json6[itemName]['lore']))
        
        if itemName in parse_json6:
            if parse_json6[itemName]['internalName'] in allCharms:
                # charms info
                print("{} is a {} charm you obtain from the raid {}, and {} requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['dropMeta']['name'], itemName, parse_json6[itemName]['requirements']['level']))
                divider()
                if "identifications" in parse_json6[itemName]:
                    print("{}'s bonus stats are:".format(itemName))
                    for itemIdentifications in parse_json6[itemName]['identifications']:
                        print(" ")
                        if itemIdentifications == "xpBonus":
                            print("{}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                        else:
                            print("Bonus {}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                    print(" ")
            elif "type" in parse_json6[itemName]:
                if parse_json6[itemName]['type'] in allWeaponTypes:
                    # weapon info
                    if "powderSlots" in parse_json6:
                        print("{} is a {} {} with {} attack speed, {} powder slots and requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'].capitalize(), parse_json6[itemName]['type'].capitalize(), parse_json6[itemName]['attackSpeed'].replace('_', ' '), parse_json6[itemName]['powderSlots'], parse_json6[itemName]['requirements']['level']))
                    else:
                        print("{} is a {} {} with {} attack speed and requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'].capitalize(), parse_json6[itemName]['type'].capitalize(), parse_json6[itemName]['attackSpeed'].replace('_', ' '), parse_json6[itemName]['requirements']['level']))
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
                    if "averageDPS" in parse_json6[itemName]['base']:
                        print("{}'s base average DPS is {}".format(itemName, parse_json6[itemName]['base']['averageDPS']))
                        divider()
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
                                dmgTypesLen = len(itemAllDamageTypes)
                                dmgTypesNum = 0
                                for i in range(dmgTypesLen):
                                    print("{}".format(itemAllDamageTypes[dmgTypesNum]))
                                    dmgTypesNum += 1
                            divider()
                    if "identifications" in parse_json6[itemName]:
                        print("{}'s bonus stats are:".format(itemName))
                        for itemIdentifications in parse_json6[itemName]['identifications']:
                            print(" ")
                            if itemIdentifications == "xpBonus" or itemIdentifications in allRawStats:
                                print("{}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                            else:
                                print("Bonus {}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                        print(" ")
                    if "lore" in parse_json6[itemName]:
                        divider()
                        print("{}'s lore says: {}".format(itemName, parse_json6[itemName]['lore']))
                elif parse_json6[itemName]['type'] in allArmorTypes:
                    # armor info
                    if parse_json6[itemName]['type'] == "boots" or parse_json6[itemName]['type'] == "leggings":
                        print("{} is a pair of {} {} that requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['type'], parse_json6[itemName]['requirements']['level']))
                    else:
                        print("{} is a {} {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['type']))
                    divider()
                    if "base" in parse_json6[itemName]:
                        print("{}'s stats are:".format(itemName))
                        print(" ")
                        for itemStats in parse_json6[itemName]['base']:
                            print("{}: {}".format(itemStats, parse_json6[itemName]['base'][itemStats]))
                        divider()
                    allRequirements = []
                    for allItemRequirements in parse_json6[itemName]['requirements']:
                        if allItemRequirements != "level":
                            allRequirements.append(allItemRequirements)
                    if allRequirements != []:
                        print("{}'s other requirements are:".format(itemName))
                        print(" ")
                        for itemRequirements in parse_json6[itemName]['requirements']:
                            if itemRequirements != "level":
                                print("{}: {}".format(itemRequirements.capitalize(), parse_json6[itemName]['requirements'][itemRequirements]))
                    if "identifications" in parse_json6[itemName]:
                        print("{}'s bonus stats are:".format(itemName))
                        for itemIdentifications in parse_json6[itemName]['identifications']:
                            print(" ")
                            if itemIdentifications == "xpBonus":
                                print("{}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                            else:
                                print("Bonus {}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                        print(" ")
                    if "lore" in parse_json6[itemName]:
                        divider()
                        print("{}'s lore says: {}".format(itemName, parse_json6[itemName]['lore']))
                elif parse_json6[itemName]['type'] in allAccessoryTypes:
                    # accessory info
                    print("{} is a {} {} that requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['accessoryType'], parse_json6[itemName]['requirements']['level']))
                    divider()
                    if "base" in parse_json6[itemName]:
                        print("{}'s stats are:".format(itemName))
                        print(" ")
                        for itemStats in parse_json6[itemName]['base']:
                            print(itemStats)
                            divider()
                    allRequirements = []
                    for allItemRequirements in parse_json6[itemName]['requirements']:
                        if allItemRequirements != "level":
                            allRequirements.append(allItemRequirements)
                    if allRequirements != []:
                        print("{}'s requirements are:".format(itemName))
                        print(" ")
                        for itemRequirements in parse_json6[itemName]['requirements']:
                            if itemRequirements != "level":
                                print(itemRequirements)
                    if "identifications" in parse_json6[itemName]:
                        print("{}'s bonus stats are:".format(itemName))
                        for itemIdentifications in parse_json6[itemName]['identifications']:
                            print(" ")
                            if itemIdentifications == "xpBonus":
                                print("{}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                            else:
                                print("Bonus {}: {}".format(itemIdentifications, parse_json6[itemName]['identifications'][itemIdentifications]))
                        print(" ")
                    if "lore" in parse_json6[itemName]:
                        divider()
                        print("{}'s lore says: {}".format(itemName, parse_json6[itemName]['lore']))
            elif "tomeType" in parse_json6[itemName]:
                # tome info
                if parse_json6[itemName]['raidReward'] == False:
                    print("{} is a {} tome that requires you to have atleast combat level {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['requirements']['level']))
                else:
                    print("{} is a {} tome that requires you to have atleast combat level {} and that you can obtain from {}".format(itemName, parse_json6[itemName]['tier'], parse_json6[itemName]['requirements']['level'], parse_json6[itemName]['dropMeta']['name']))
                itemRequirementsStatsAndIdentifications()
            elif "ingredientPositionModifiers" in parse_json6[itemName]:
                # ingredient info
                def ingredientInfoDef(a, b, c):
                    if parse_json6[itemName][a][b] < 0:
                        print("{} decreases the {} of an item by {}".format(itemName, c, parse_json6[itemName]['itemOnlyIDs']['durabilityModifier']))
                    elif parse_json6[itemName][a][b] > 0:
                        print("{} increases the {} of an item by {}".format(itemName, c, parse_json6[itemName]['itemOnlyIDs']['durabilityModifier']))
                    else:
                        print("{} doesnt change the {} of an item".format(itemName, c))
                    divider()
                print("{} is a tier {} material".format(itemName, parse_json6[itemName]['tier']))
                print("that is dropped by:")
                for mobThatDropsItem in parse_json6[itemName]['droppedBy']:
                    print(mobThatDropsItem)
                divider()
                print("{} requires you to have atleast level {} in:".format(itemName, parse_json6[itemName]['requirements']['level']))
                for skillRequirement in parse_json6[itemName]['requirements']['skills']:
                    print(skillRequirement.capitalize())
                divider()
                ingredientInfoDef('itemOnlyIDs', 'durabilityModifier', 'durability')
                ingredientInfoDef('consumableOnlyIDs', 'duration', 'duration')
                ingredientInfoDef('consumableOnlyIDs', 'charges', 'charges')
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
                # resource info
                print("{} is a tier 2 resource that requires you to have atleast {} level {}, and you can use it to make:".format(itemName, parse_json6[itemName]['requirements']['skills'], parse_json6[itemName]['requirements']['level']))
                for craftableItems in parse_json6[itemName]['craftable']:
                    print(craftableItems.capitalize())
        else:
            print("Sorry but the word you typed in is not in the database, please try again once the program restarts itself")
            time.sleep(3)
            divider()
            continue
        
        continue
    elif choice.lower() == "t":
        # territory info
        territoryAPI = requests.get("{}guild/list/territory".format(wynncraftAPI))

        territoryData = territoryAPI.text

        parse_json7 = json.loads(territoryData)

        print("Please type in a letter that corresponds with what you want to view: ")
        divider()
        print("h = how many territories does a guild owns")
        print("i = info on a specific territory")
        print("e = exit")
        divider()

        choice3 = input()
        divider()

        if choice3.lower() == "h":
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
            territoryDict = {}
            for i in range(len(territoryGuildNames)):
                territoryDict[territoryGuildNames[n]] = guildNum[n]
                n += 1
            for key, value in dict(sorted(territoryDict.items(), key=lambda x:x[1], reverse=True)).items():    
                print(" ")
                print("The guild", key, "owns", value, "territories")
            print(" ")
            divider()
        elif choice3.lower() == "i":
            territoryName = input("Please type in the name of the territory you want to view info about: ")
            divider()
            territoryName = string.capwords(territoryName, sep=None)
            if territoryName in parse_json7:
                print("Succesfully found a territory by the name {}".format(territoryName))
                divider()
            else:
                print("Sorry but there doesnt seem to be a territory called {}, please try again once the program restarts itself".format(territoryName))
                time.sleep(3)
                divider()
                continue

            arr = []
            arr2 = []
            for date in parse_json7[territoryName]['acquired']:
                arr.append(date)
            x = 0
            for i in range(10):
                arr2.append(arr[x])
                x += 1
            x = 0
            for i in range(len(arr2)):
                if arr2[x] == "-":
                    arr2.pop(x)
                else:
                    x += 1
            easyDates = []
            x = 0
            while x <= 3:
                easyDates.append(arr2[x])
                x += 1
            easyDate1 = ''.join(easyDates)
            easyDates.clear()
            while x >= 4 and x <= 5:
                easyDates.append(arr2[x])
                x += 1
            easyDate2 = ''.join(easyDates)
            easyDates.clear()
            while x >= 6 and x <= 7:
                easyDates.append(arr2[x])
                x += 1
            x = 0
            if easyDates[1] == "1":
                x = 1
            elif easyDates[1] == "2":
                x = 2
            elif easyDates[1] == "3":
                x = 3
            else:
                x = 4
            easyDate3 = ''.join(easyDates)
            easyDates.clear()
            monthsDict = {
                "01": 'January',
                "02": 'February',
                "03": 'March',
                "04": 'April',
                "05": 'May',
                "06": 'June',
                "07": 'July',
                "08": 'August',
                "09": 'September',
                "10": 'October',
                "11": 'November',
                "12": 'December'
            }
            easyDate3 = int(easyDate3)

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

            if x == 1:
                print("The owner of the territory you are currently looking at ({}) is {} aka {} and they acquired the territory on the {}st of {} {}".format(territoryName, parse_json7[territoryName]['guild']['name'], parse_json7[territoryName]['guild']['prefix'], easyDate3, monthsDict[easyDate2], easyDate1))
            elif x == 2:
                print("The owner of the territory you are currently looking at ({}) is {} aka {} and they acquired the territory on the {}nd of {} {}".format(territoryName, parse_json7[territoryName]['guild']['name'], parse_json7[territoryName]['guild']['prefix'], easyDate3, monthsDict[easyDate2], easyDate1))
            elif x == 3:
                print("The owner of the territory you are currently looking at ({}) is {} aka {} and they acquired the territory on the {}rd of {} {}".format(territoryName, parse_json7[territoryName]['guild']['name'], parse_json7[territoryName]['guild']['prefix'], easyDate3, monthsDict[easyDate2], easyDate1))
            else:
                print("The owner of the territory you are currently looking at ({}) is {} aka {} and they acquired the territory on the {}th of {} {}".format(territoryName, parse_json7[territoryName]['guild']['name'], parse_json7[territoryName]['guild']['prefix'], easyDate3, monthsDict[easyDate2], easyDate1))
            divider()
        elif choice3.lower() == "e":
            quit()
        else:
            print("Sorry, what you wrote is not associated with any category, please try again once the program closes itself")
            time.sleep(3)
            divider()
            continue

        continue
    elif choice.lower() == "c":
        os.system('cls')
    elif choice.lower() == "e":
        quit()
    else:
        print("Sorry, what you wrote is not associated with any category, please try again")
        time.sleep(3)
        divider()
        continue
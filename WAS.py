import requests
import json
import time
import os
import string
import datetime

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
    print("i = item database (doesnt work rn sorry ;w;)")
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

        monthsAndYearsLengthDict = {
            "January": 31,
            "February1": 28,
            "February2": 29,
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31,
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31,
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        leap = False

        now = datetime.datetime.now()
        now = str(now)

        arr = []
        arr2 = []
        x = 0
        for letters in now:
            arr.append(letters)
        for i in range(10):
            arr2.append(arr[x])
            x += 1
        easyDate = ''.join(arr2)
        arr = []
        arr2 = []
        x = 0
        for letters in parse_json4['lastJoin']:
            arr.append(letters)
        for i in range(10):
            arr2.append(arr[x])
            x += 1
        easyDate4 = ''.join(arr2)
        easyDate4 = easyDate4.replace("-", "")
        arr = []
        arr2 = []
        arr3 = []
        x = 0
        for i in range(4):
            arr.append(easyDate4[x])
            x += 1
        for i in range(2):
            arr2.append(easyDate4[x])
            x += 1
        for i in range(2):
            arr3.append(easyDate4[x])
            x += 1
        targetYear = ''.join(arr)
        targetMonth = ''.join(arr2)
        targetDay = ''.join(arr3)
        targetYear = int(targetYear)
        targetMonth = int(targetMonth)
        targetDay = int(targetDay)
        arr = []
        arr2 = []
        arr3 = []
        x = 0
        y = 1
        z = 0
        for letters in easyDate:
            arr.append(letters)
        for letters in arr:
            if arr[x] == "-":
                arr.pop(x)
            else:
                x += 1
        easyDate = ''.join(arr)
        arr = []
        x = 0
        for letters in easyDate:
            if z == 0:
                if len(arr) == 4:
                    y += 1
                    z += 1
                    x = 0
            elif z == 1:
                if len(arr2) == 2:
                    y += 1
                    z += 1
                    x = 0
            elif z == 2:
                if len(arr3) == 2:
                    y += 1
                    z += 1
                    x = 0
            if y == 1:
                if x <= 3:
                    arr.append(letters)
            elif y == 2:
                if x <= 1:
                    arr2.append(letters)
            elif y == 3:
                if x <= 1:
                    arr3.append(letters)
            x += 1
        year = ''.join(arr)
        month = ''.join(arr2)
        day = ''.join(arr3)
        year = int(year)
        month = int(month)
        day = int(day)
        yearCount = 0
        monthCount = 0
        dayCount = 0
        while True:
            if year == targetYear and month == targetMonth and day == targetDay:
                break
            day -= 1
            if day == 0:
                month -= 1
                if monthCount > 0:
                    monthCount += 1
                dayCount = 0
                if month == 0:
                    month = 12
                    day = monthsAndYearsLengthDict["December"]
                    year -= 1
                    continue
                if year % 4 == 0:
                    leap = True
                else:
                    leap = False
                if month == 2:
                    if leap == True:
                        day = monthsAndYearsLengthDict["February2"]
                    elif leap == False:
                        day = monthsAndYearsLengthDict["February1"]
                elif month != 2:
                    month2 = monthsAndYearsLengthDict[month]
                    day = monthsAndYearsLengthDict[month2]

        today = int(datetime.datetime.now().strftime("%d"))
        thisMonth = datetime.datetime.now().strftime("%B")
        if thisMonth == "February":
            if int(datetime.datetime.now().strftime("%Y")) % 4 == 2:
                thisMonth == "February2"
            else:
                thisMonth == "February1"
        if day > today:
            dayCount = monthsAndYearsLengthDict[thisMonth] - day
        elif today > day:
            dayCount = today - day
        elif today == day:
            dayCount = 0
        while monthCount >= 12:
            monthCount -= 12
            yearCount += 1

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
            print(f"{playerName} is currently offline but were last online {yearCount} year(s), {monthCount} month(s) and {dayCount} day(s) ago")

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
        itemTypes = []
        charms = []
        itemNames = []
        itemJson = json.loads(requests.get("https://beta-api.wynncraft.com/v3/item/database?fullResult").text)
        for types in itemJson:
            if 'type' in itemJson[types]:
                itemTypes.append(itemJson[types]['type'])
            else:
                charms.append(itemJson[types]['internalName'])
        itemTypes = list(dict.fromkeys(itemTypes))
        for items in itemJson:
            itemNames.append(items.lower())

        itemName = input("Please type in the name of the item you want to view info on: ")
        itemName = string.capwords(itemName)
        divider()

        lettersList = []
        for letters in itemName:
            lettersList.append(letters)

        x = 0
        y = 0
        for letters in lettersList:
            if lettersList[x] == "-":
                y = x+1
                lettersList[y] = lettersList[y].upper()
            x += 1
        itemName = ''.join(lettersList)
        lettersList.clear()

        itemName = itemName.replace("Of", "of").replace("The", "the")
        internalItemName = itemJson[itemName]['internalName']
        findItem = itemJson[itemJson[itemName]['internalName']]

        def itemInfo(isWeapon, itemType):
            if 'type' in findItem:
                # prints out the info about the items powder slots, dps, rarity, type and drop restrictions
                if 'powderSlots' in itemJson[itemName]:
                    if itemJson[itemName]['dropRestriction'] == "never":
                        if itemJson[itemName]['powderSlots'] == 1:
                            if isWeapon == True:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slot that never drops from mobs, that also has {itemJson[itemName]['attackSpeed']} attack speed")
                            else:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slot that never drops from mobs")    
                        elif itemJson[itemName]['powderSlots'] > 1:
                            if isWeapon == True:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slots that never drops from mobs, that also has {itemJson[itemName]['attackSpeed']} attack speed")
                            else:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slots that never drops from mobs")  
                        else:
                            if isWeapon == True:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with no powder slots that also never drops from mobs, that also has {itemJson[itemName]['attackSpeed']} attack speed")
                            else:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} no powder slots also that never drops from mobs")  
                    else:
                        if itemJson[itemName]['powderSlots'] == 1:
                            if isWeapon == True:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slot, that also has {itemJson[itemName]['attackSpeed']} attack speed")
                            else:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slot")
                        elif itemJson[itemName]['powderSlots'] > 1:
                            if isWeapon == True:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slots, that also has {itemJson[itemName]['attackSpeed']} attack speed")
                            else:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} powder slots")
                        else:
                            if isWeapon == True:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with no powder slots, that also has {itemJson[itemName]['attackSpeed']} attack speed")
                            else:
                                print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} with {itemJson[itemName]['powderSlots']} no powder slots")
                else:
                    if itemJson[itemName]['type'] == "accessory":
                        if itemJson[itemName]['dropRestriction'] == "lootchest":
                            print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} that you can find in chests")
                        else:
                            print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} that doesnt appear in chests")
                    elif itemJson[itemName]['type'] == "tome":
                        if itemJson[itemName][itemType] == "guild_tome" or itemJson[itemName]['raidReward'] == False:
                            print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType].replace('_', ' ')}")
                        else:
                            print(f"{internalItemName} is a {itemJson[itemName]['rarity']} {itemJson[itemName][itemType]} that you can get from raids")
                    elif itemJson[itemName]['type'] == "charm":
                        print(f"{internalItemName} is a {itemJson[itemName]['rarity']} charm that you can get from the {itemJson[itemName]['dropMeta']['name']} raid")
                if isWeapon == True:
                    print(f"and {internalItemName}'s base average dps is {itemJson[itemName]['averageDps']}")
                divider()
                if 'lore' in findItem:
                    # find and print the description of the item
                    print(f"{internalItemName}'s description says:")
                    print(" ")
                    print(f'"{itemJson[itemName]["lore"]}"')
                    print(" ")
                    divider()
                if 'base' in findItem:
                    # find and print the base stats the item gives
                    print(f"{internalItemName}'s base stats are:")
                    baseStatsListNames = []
                    baseStatsList = []
                    baseStats = {}
                    for stats in itemJson[itemName]['base']:
                        baseStatsListNames.append(stats)
                    x = 0
                    for i in range(len(baseStatsListNames)):
                        baseStatsList.append(itemJson[itemName]['base'][baseStatsListNames[x]])
                        baseStats[baseStatsListNames[x]] = baseStatsList[x]
                        x += 1
                    baseStatsList.clear()
                    baseStatsListNames.clear()
                    print(" ")
                    for key, value in baseStats.items():
                        print(f"{key.replace('base', '')}: {value}")
                    print(" ")
                    divider()
                if 'requirements' in findItem:
                    # finds the items requirements and prints them out
                    requirementsList = []
                    for requirements in itemJson[itemName]['requirements']:
                        requirementsList.append(requirements)
                    requirementsList.remove("level")
                    if requirementsList != []:
                        print(f"You have to be combat level {itemJson[itemName]['requirements']['level']} in order to use {internalItemName} and also have:")
                        print(" ")
                        if isWeapon == True:
                            requirementsList.remove("classRequirement")
                        requirementsList2 = []
                        for i in range(0, len(requirementsList)):
                            requirementsList2.append(itemJson[itemName]['requirements'][requirementsList[i]])
                        requirementsDict = {}
                        for i in range(0, len(requirementsList)):
                            requirementsDict[requirementsList[i]] = requirementsList2[i]
                        requirementsList.clear()
                        requirementsList2.clear()
                        for key, value in requirementsDict.items():
                            print(f"{value} {key}")
                        print(" ")
                    else:
                        print(f"You have to be combat level {itemJson[itemName]['requirements']['level']} in order to use {internalItemName}")
                    divider()
                if 'identifications' in findItem:
                    # finds the items id's and also prints them out
                    identificationList = []
                    for id in itemJson[itemName]['identifications']:
                        identificationList.append(id)
                    minMaxValue = []
                    idDict = {}
                    for i in range(len(identificationList)):
                        identification = itemJson[itemName]['identifications'][identificationList[i]]
                        try:
                            minMaxValue.append(identification['min'])
                            minMaxValue.append(identification['max'])
                            try:
                                idDict[identificationList[i]] = minMaxValue
                            except IndexError:
                                break
                            minMaxValue = []
                        except TypeError:
                            pass
                    print(" ")
                    for key, value in idDict.items():
                        print(f"The minimal amount of {key} you can get is: {value[0]}")
                        print(f"The maximum amount of {key} you can get is: {value[1]}")
                        print(" ")
                    divider()

        if itemName.lower() not in itemNames:
            print(f"Sorry but the item name {itemName} isnt in the database, please try again")
            continue

        itemType2 = str(itemJson[itemName]['type'] + 'Type')

        if itemJson[itemName]['type'] == "weapon":
            itemInfo(True, itemType2)
        else:
            itemInfo(False, itemType2)
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

import requests
import json
import time

def space():
    print(" ")
def divider():
    print("-------------------------------------------------------------------------------------------------------")

print("Please type in the letter that corresponds with what you want to see")
print("g = guild info")
divider()

choice = input()

divider()
if choice == "g" or choice == "G":
    guildnameinput = str(input("Please type in the name of the guild you want to view the info of: "))
    
    GuildAPI = requests.get("https://api.wynncraft.com/v3/guild/{}".format(guildnameinput))

    guild_data = GuildAPI.text

    parse_json = json.loads(guild_data)

    # Checks if the guild exists
    if parse_json['name'] == None:
        divider()
        print("The guild you are looking for doesnt exist")
        print("Please try again by restarting this program")
        time.sleep(10)
        quit()
    else:
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
        GuildAPI = requests.get("https://api.wynncraft.com/v3/guild/{}".format(guildnameinput))

        guild_data = GuildAPI.text

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
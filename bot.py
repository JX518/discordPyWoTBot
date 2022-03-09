from collections import deque
from re import search
from this import d
from aiohttp import client
import discord
from discord import activity
from discord.ext.commands.core import command
from discord.player import FFmpegAudio
import requests
import datetime

class WoT:
    def getPlayers(search: str) -> dict:
        URL = "https://api.worldoftanks.com/wot/account/list/?application_id=a5c99768df871fa42a0b10a16e8e89ca&search=" + search +"&type=startswith"
        data = requests.get(url = URL, params = None).json()
        return data

    

class MyClient(discord.Client):

    #Starts the bot and outputs ready.
    async def on_ready(self):
        print('Logged on as', self.user)  

    #detects messages from other authors
    async def on_message(self, message):
        #spam bot mode
        """if message.author == self.user:
            await message.channel.send('@everyone')"""
        #Commands only specific to JX (dev)
        if 267998423611998210 == message.author.id and isinstance(message.channel, discord.channel.DMChannel):
            arr = message.content.split(" ")
            
            if arr[0] == "-msgChannel" and len(arr) > 2:
                msgArr = message.content.split(" ", 2) 
                channelID = int(msgArr[1])
                #print("ChannelID:", channelID, type(channelID))
                channel = client.get_channel(channelID)
                await channel.send(msgArr[2])

        #don't respond to ourselves  
        if  message.author == self:
            return 

        #Tests if the bot works properly
        if message.content == 'test':
            await message.channel.send('true') 

        #If the message begins with the command prefix, it checks if the message is a command.
        if message.content[0] == "-": 
            #string[start:end:step]

            if(message.content[1:7].lower() == "search"):
                arr = message.content.split(" ")
                
                try:
                    search = arr[1]
                except IndexError:
                    if(len(message.content) == 7):
                        await message.channel.send("-search [partOfUsername]")
                        return
                
                URL = "https://api.worldoftanks.com/wot/account/list/?application_id=a5c99768df871fa42a0b10a16e8e89ca&search=" + arr[1] +"&type=startswith"
                data = requests.get(url = URL, params = None).json()
                
                try:
                    if(data['meta']['count'] == 100):
                        output = str(data['meta']['count']) + "+ results found"
                    else:
                        output = str(data['meta']['count']) + " results found"
                    for player in data['data']:
                        output = output + "\n" + player['nickname']
                    await message.channel.send(output)
                #if there is no data[meta][count] this error will generate 
                # because there are too many or too little players
                except KeyError:
                    if(data['error']['message'] == 'NOT_ENOUGH_SEARCH_LENGTH'):
                        await message.channel.send("Searches must have a minimum of 3 characters")
                    if(data['error']['message'] == 'INVALID_SEARCH'):   
                        await message.channel.send("0 results found") 
                    return   

            if(message.content[1:6].lower() == "stats"):
                arr = message.content.split(" ")
                try:
                    test = arr[1]
                except IndexError:
                    await message.channel.send("-stats [username]")
                    return
                URL = "https://api.worldoftanks.com/wot/account/list/?application_id=a5c99768df871fa42a0b10a16e8e89ca&search=" + arr[1] +"&type=startswith"
                data = requests.get(url = URL, params = None).json()
                try:
                    for player in data['data']:
                        if(player['nickname'].lower() == arr[1].lower()):
                            ID = player['account_id']
                            break
                except KeyError:
                    if(len(arr[1]) < 3):
                        await message.channel.send(arr[1] + "is too short")
                    else:
                        await message.channel.send("No player with the username " + arr[1])
                    return

                try: 
                    type(ID)
                except UnboundLocalError:
                    await message.channel.send("No player with the username " + arr[1])
                    return

                URL = "https://api.worldoftanks.com/wot/account/info/?application_id=a5c99768df871fa42a0b10a16e8e89ca&account_id=" + str(ID)
                data = requests.get(url = URL, params = None).json()
                tmp = data['data'][str(ID)]
                sendStr = "\nLast Battle Time: " + str(datetime.datetime.fromtimestamp(tmp['last_battle_time'])) + "\nCreated At: " + str(datetime.datetime.fromtimestamp(tmp['created_at'])) + "\nUpdated At: " + str(datetime.datetime.fromtimestamp(tmp['updated_at'])) + "\nLast Logged Out At: " + str(datetime.datetime.fromtimestamp(tmp['logout_at']))
                await message.channel.send(sendStr)   
                print(data['data'][str(ID)]['statistics']['all'])
                #todo: get stas from data['data'][str(ID)]['statistics']['all']

client = MyClient() 
#this client.run('token')
client.run('ODI2MjU3MTAwMzU0NDg2MzAz.YGJ14w._QdDCVnpyV8y_y0yiWeuCt1SJek') 
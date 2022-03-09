# from collections import deque
# from re import search
# from this import d
# from aiohttp import client
from dataclasses import dataclass
from email.mime import image
from tkinter import font
from turtle import color
import discord
# from discord import activity
# from discord.ext.commands.core import command
# from discord.player import FFmpegAudio
import requests
import datetime
from WoTAPI import WoTAPI as WoT

class methods:
    def mostPlayedTanks(tankStats:dict) -> dict:
        notInOrder = True
        while(notInOrder):
            for i in range(len(tankStats)-1):
                notInOrder = False
                if(tankStats[i]['statistics']['battles'] < tankStats[i+1]['statistics']['battles']):
                    tmp = tankStats[i]
                    tankStats[i] = tankStats[i + 1]
                    tankStats[i + 1] = tmp
                    notInOrder = True
        return tankStats
            


class MyClient(discord.Client):
    wot:WoT = None

    #Starts the bot and outputs ready.
    async def on_ready(self):
        print('Logged on as', self.user) 
        #create a global WoT API variable
        MyClient.wot:WoT = WoT("a5c99768df871fa42a0b10a16e8e89ca")

    #detects messages from other authors
    async def on_message(self, message):
        #spam bot mode
        
        """if message.author == self.user:
            await message.channel.send('@everyone')"""

        #don't respond to ourselves  
        if  message.author == self.user:
            return

        #Tests if the bot works properly
        if message.content == 'test':
            msg = discord.Embed(title = "title", description = "description a\nb cd", color = 0xff0000)
            await message.channel.send(embed = msg) 

        #If the message begins with the command prefix, it checks if the message is a command.
        if message.content != "" and message.content[0] == "-": 
            #string[start:end:step]
            if(message.content[1:7].lower() == "search"):
                arr = message.content.split(" ")
                try:
                    search = arr[1]
                except IndexError:
                    if(len(message.content) == 7):
                        msg = discord.Embed(title = "Syntax Error", description = "-search [partOfUsername]", color = 0xff0000)
                        await message.channel.send(embed = msg)
                        return
                        
                data = MyClient.wot.getPlayers(arr[1])
                
                try:
                    players:str = ""
                    if(data['meta']['count'] == 100):
                        output = str(data['meta']['count']) + "+ results found"
                    else:
                        output = str(data['meta']['count']) + " results found"
                        msg = discord.Embed(title = output, color = 0x00aa00)
                    for player in data['data']:
                        players = players + "\n" + player['nickname']
                    playersArr = players.split("_")
                    players = playersArr[0]
                    for i in range(1,len(playersArr)):
                        players = players + "\_" + playersArr[i]

                    msg = discord.Embed(title = output, description = players, color = 0x00aa00)
                    await message.channel.send(embed = msg)
                #if there is no data[meta][count] this error will generate 
                # because there are too many or too little players
                except KeyError:
                    if(data['error']['message'] == 'NOT_ENOUGH_SEARCH_LENGTH'):
                        msg = discord.Embed(title = "Search Length Error", description = "Searches must have a minimum of 3 characters", color = 0xff0000)
                        await message.channel.send(embed = msg)
                    if(data['error']['message'] == 'INVALID_SEARCH'):                          
                        msg = discord.Embed(title = "0 results found", color = 0x00aa00)
                        await message.channel.send(embed = msg)
                    return   

            if(message.content[1:6].lower() == "stats"):
                arr = message.content.split(" ")
                try:
                    test = arr[1]
                except IndexError:
                    msg = discord.Embed(title = "Syntax Error", description = "-stats [FullUsername]", color = 0xff0000)
                    await message.channel.send(embed = msg)
                    return
                
                data = MyClient.wot.getPlayers(test)
                try:
                    ID = MyClient.wot.getID(test)
                except: 
                    pass

                try: 
                    type(ID)
                except UnboundLocalError:
                    msg = discord.Embed(title = "No player with the username " + test, color = 0x00aa00)
                    await message.channel.send(embed = msg)
                    return

                strID = str(ID)
                data = MyClient.wot.getPlayerStats(account_id = strID)
                try:
                    tmp = data['data'][strID]
                except KeyError:
                    usernameArr = test.split("_")
                    test = usernameArr[0]
                    for i in range(1,len(usernameArr)):
                        test = test + "\_" + usernameArr[i]
                    msg = discord.Embed(title = "No player with the username " + test, color=0xff0000)
                    await message.channel.send(embed = msg)
                # sendStr = "\nLast Battle Time: " + str(datetime.datetime.fromtimestamp(tmp['last_battle_time'])) + "\nCreated At: " + str(datetime.datetime.fromtimestamp(tmp['created_at'])) + "\nUpdated At: " + str(datetime.datetime.fromtimestamp(tmp['updated_at'])) + "\nLast Logged Out At: " + str(datetime.datetime.fromtimestamp(tmp['logout_at'])) + "\n\n"
                try:
                    username = data['data'][strID]['nickname']
                except KeyError:
                    msg = discord.Embed(title = "No player with the username " + test, color=0xff0000)
                    await message.channel.send(embed = msg)
                    return
                battles = data['data'][strID]['statistics']['all']['battles']
                data = MyClient.wot.getTankStats(account_id = strID)
                tanks = methods.mostPlayedTanks(data['data'][strID])
                sendStr = "Top Most Played Tanks (" + str(battles) + " Battles Total): \n"
                sendStr = sendStr + MyClient.wot.tankFromID(str(tanks[0]['tank_id'])) + " --- (" + str(tanks[0]['statistics']['battles']) + " battles, " + "{:.2f}".format(100*(tanks[1]['statistics']['wins']/tanks[1]['statistics']['battles'])) + "% winrate)" + "\n" 
                try:
                    sendStr = sendStr + MyClient.wot.tankFromID(str(tanks[1]['tank_id'])) + " --- (" + str(tanks[1]['statistics']['battles']) +  " battles, " + "{:.2f}".format(100*(tanks[1]['statistics']['wins']/tanks[1]['statistics']['battles'])) + "% winrate)" + "\n" 
                except:
                    sendStr = sendStr+"n/a\n"
                try: 
                    sendStr = sendStr + MyClient.wot.tankFromID(str(tanks[2]['tank_id'])) + " --- (" + str(tanks[2]['statistics']['battles']) + " battles, " + "{:.2f}".format(100*(tanks[2]['statistics']['wins']/tanks[2]['statistics']['battles'])) + "% winrate)" 
                except:
                    sendStr = sendStr+"n/a\n"
                usernameArr = username.split("_")
                username1 = usernameArr[0]
                for i in range(1,len(usernameArr)):
                    username1 = username1 + "\_" + usernameArr[i]
                msg = discord.Embed(title = username1, description = sendStr, color = 0x00aa00, url = "https://wotlabs.net/na/player/" + username)
                msg.set_image(url = "http://wotlabs.net/sig_dark/na/"+username+"/signature.png")
                await message.channel.send(embed = msg)
                
client = MyClient() 
#this client.run('token')
client.run('ODI2MjU3MTAwMzU0NDg2MzAz.YGJ14w._QdDCVnpyV8y_y0yiWeuCt1SJek') 
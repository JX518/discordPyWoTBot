from ast import If
from cmath import e
from collections import deque
from ctypes import Array
import threading
from re import search
from this import d

from numpy import array
from urllib3 import Timeout
from aiohttp import client
from dataclasses import dataclass
import discord
from discord import activity
from discord.channel import VoiceChannel
from discord.embeds import Embed
from discord.errors import ClientException
# import youtube_dl (youtube_dl is outdated)
import yt_dlp as youtube_dl
from discord.ext.commands.core import command
from discord.player import FFmpegAudio
import requests
import datetime
from WoTAPI import WoTAPI as WoT
import os
import time

class methods:
    '''
    music_queue
        [
            (song)[
                embed
                songFileName
            ]
        ]
    '''
    
    def play(music_queue: Array, voiceChannel: VoiceChannel, voice):
        if(len(music_queue)>0):
            music_queue[0]
    
    #creates the video URL 
    def getVideo(search: str) -> dict:
        if("https://youtu.be/" in search or "https://www.youtube.com/watch?v=" in search):
            url = search
        else:
            YTAPIKey:str = "AIzaSyDC_3dXyozYOdY9_d7e6y3UJPUhPFExvXs"
            Video = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&order=relevance&q="+ search +"&safeSearch=none&key=" + YTAPIKey
            VidData = requests.get(url = Video).json()
            VID = VidData['items'][0]['id']['videoId']
            url = "https://www.youtube.com/watch?v=" + VID
        
        #creates the video embed
        videoName = VidData['items'][0]['snippet']['title']
        emb = Embed(title = "Playing: ", description = videoName, color=0x00aa00, url = url)
        emb.set_thumbnail(url = VidData['items'][0]['snippet']['thumbnails']['default']['url'])
        
        ydl_opts = {
                        'format':'bestaudio/best',
                        'postprocessors':[{
                            'key':'FFmpegExtractAudio',
                            'preferredcodec':'mp3',
                            'preferredquality':'192',
                        }],
                    }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl: 
            ydl.download([url])
            
        # print(VidData['items'][0]['id']['videoId'])
        
        songDict = {
            'embed': emb,
            'ID': VidData['items'][0]['id']['videoId']
        }
        
        return songDict
        
        
    
    def mostPlayedTanks(tankStats:dict) -> dict:
        notInOrder = True
        if(len(tankStats)>2):
            while(notInOrder):
                for i in range(len(tankStats)-1):
                    notInOrder = False
                    if(tankStats[i]['statistics']['battles'] < tankStats[i+1]['statistics']['battles']):
                        tmp = tankStats[i]
                        tankStats[i] = tankStats[i + 1]
                        tankStats[i + 1] = tmp
                        notInOrder = True
        if(len(tankStats)==2):
            if(tankStats[1]['statistics']['battles'] < tankStats[2]['statistics']['battles']):
                        tmp = tankStats[i]
                        tankStats[i] = tankStats[i + 1]
                        tankStats[i + 1] = tmp
        return tankStats

class MyClient(discord.Client):
    wot:WoT = None
    music_queue = []

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
                if(len(test) < 3):
                    msg = discord.Embed(title = "No player with the username " + test, color = 0x00aa00)
                    await message.channel.send(embed = msg)
                    return
                ID = MyClient.wot.getID(test)

                
                print (ID)
                
                if(ID == None):
                    print("none")
                    msg = discord.Embed(title = "No player with the username " + test, color = 0x00aa00)
                    await message.channel.send(embed = msg)
                    return

                strID = str(ID)
                data = MyClient.wot.getPlayerStats(account_id = strID)
                # try:
                tmp = data['data'][strID]
                # except KeyError:
                #     usernameArr = test.split("_")
                #     test = usernameArr[0]
                #     for i in range(1,len(usernameArr)):
                #         test = test + "\_" + usernameArr[i]
                #     msg = discord.Embed(title = "No player with the username " + test, color=0xff0000)
                #     await message.channel.send(embed = msg)
                # sendStr = "\nLast Battle Time: " + str(datetime.datetime.fromtimestamp(tmp['last_battle_time'])) + "\nCreated At: " + str(datetime.datetime.fromtimestamp(tmp['created_at'])) + "\nUpdated At: " + str(datetime.datetime.fromtimestamp(tmp['updated_at'])) + "\nLast Logged Out At: " + str(datetime.datetime.fromtimestamp(tmp['logout_at'])) + "\n\n"
                
                # try:
                username = data['data'][strID]['nickname']
                # except KeyError:
                #     msg = discord.Embed(title = "No player with the username " + test, color=0xff0000)
                #     await message.channel.send(embed = msg)
                #     return
                
                battles = tmp['statistics']['all']['battles']
                data = MyClient.wot.getTankStats(account_id = strID)
                tanks = methods.mostPlayedTanks(data['data'][strID])
                sendStr = "Top Most Played Tanks (" + str(battles) + " Battles Total): \n"
                try:
                    sendStr = sendStr + MyClient.wot.tankFromID(str(tanks[0]['tank_id'])) + " --- (" + str(tanks[0]['statistics']['battles']) + " battles, " + "{:.2f}".format(100*(tanks[1]['statistics']['wins']/tanks[1]['statistics']['battles'])) + "% winrate)" + "\n" 
                except:
                    sendStr = sendStr+"n/a\n"
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

            if(message.content[1:5].lower() == "play"): 
                #joins VC if not already in a VC
                try:
                    voiceChannel = message.author.voice.channel
                except:
                    await message.channel.send(embed = Embed(title="Please Connect to a Voice Channel"), color = 0xff0000)
                
                arr = message.content.split(" ")
                song = message.content[6:len(message.content)]
                # print(song)
                
                searchData = methods.getVideo(song)
                
                await message.channel.send(embed = searchData['embed'])
                error:bool = True
                while(error == True):
                    try:
                        await voiceChannel.connect() 
                        error = False
                    except TimeoutError:
                        error = True
                voice = discord.utils.get(client.voice_clients, guild=message.guild)
                
                for file in os.listdir("./"):
                    if file.endswith(".mp3") and ("["+searchData['ID']+"]") in file:
                        if(os.path.isfile("nowPlaying.mp3")):
                            os.remove("nowPlaying.mp3")
                            os.rename(file, "nowPlaying.mp3")
                        else:
                            os.rename(file, "nowPlaying.mp3")
                        voice.play(discord.FFmpegPCMAudio("nowPlaying.mp3")) 
                        break
                
client = MyClient() 
#this client.run('token')
client.run('ODI2MjU3MTAwMzU0NDg2MzAz.YGJ14w._QdDCVnpyV8y_y0yiWeuCt1SJek') 
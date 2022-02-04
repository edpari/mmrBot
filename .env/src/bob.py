import discord
import requests
import json
import os

from dotenv import load_dotenv

def getData(uri, mode, pseudo):
    jsonReq = requests.get(uri).json()
    if jsonReq :
        ## FEATURE : ajouter d'autres donnees de la requete
        jsonMode = jsonReq[mode]['avg']
        if jsonMode :
            res = jsonMode
        else :
            res = 'Aucune donnée en mode : ' + mode + ' pour le joueur : ' + pseudo
    else :
        res = 'Pseudo introuvable : ' + pseudo
    return res

def getHelp():
    return 'HELP (liste non encore disponible)'

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.content.startswith('!mmr'):
            commands = message.content.split()
            if len(commands) == 2 and commands[1] in ['help', 'HELP', 'Help']:
                await message.channel.send(getHelp())
            elif len(commands) == 3 :
                mode = commands[1]
                ## FIXME : les pseudos avec des espaces
                pseudo = commands[2]
                if pseudo[-3:] == 'zox':
                    ## FIXME : un seul message suffirait
                    await message.channel.send('A chier Drazox')
                    requests.get(uri).json()

                ## DEBUG
                print('COMMANDE : ' + pseudo+ ' ---- ' + mode)

                uri = "https://euw.whatismymmr.com/api/v1/summoner?name=" + pseudo
                if mode in ['ranked','Ranked','solo','soloQ', 'soloq']:
                    jsonRes = getData(uri, 'ranked', pseudo)
                    await message.channel.send(jsonRes)
                elif mode in ['aram','ARAM', 'Aram']:
                    jsonRes = getData(uri, 'ARAM', pseudo)
                    await message.channel.send(jsonRes)
                elif mode in ['normale', 'normal', 'Normale', 'Normal', 'draft']:
                    jsonRes = getData(uri, 'normal', pseudo)
                    await message.channel.send(jsonRes)
                else :
                    await message.channel.send('Mode de jeu non existant, !mmr help pour connaitre la liste des commandes')
            else :
                await message.channel.send('Commande non reconnue ou pseudo avec des espaces (ntm jordan)')

## ------ Launch du client ------------      
load_dotenv(dotenv_path="config")

client = MyClient()
client.run(os.getenv("TOKEN"))
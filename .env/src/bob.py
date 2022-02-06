import discord
import requests
import json
import os
from dotenv import load_dotenv

## FEATURE : ajouter un postgres classement dans l'alliance
def getData(uri, mode, pseudo):
    jsonReq = requests.get(uri).json()
    if jsonReq :
        ## FEATURE : ajouter d'autres donnees de la requete
        jsonMode = jsonReq[mode]
        if jsonMode['avg'] :
            res = 'MMr moyen de ' + pseudo + ': ' + str(jsonMode['avg']) + '(+/- ' +str(jsonMode['err']) + ')'
        else :
            res = 'Aucune donnée en mode : ' + mode + ' pour le joueur : ' + pseudo
    ## FIXME : catch les types d'erreurs ? 500/404/401 etc
    else :
        res = 'Pseudo introuvable : ' + pseudo
    return res

def getHelp():
    print('COMMANDE : ---------------- HELP')
    rMess = 'HELP :\n'
    rMess += '!mmr <mode> <pseudo[]>\n'
    rMess += '<mode> : ranked, aram, normale\n'
    return rMess 

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
            elif len(commands) >= 3 :
                mode = commands[1]
                pseudo = ' '.join(commands[2:])
                if pseudo[-3:] == 'zox':
                    await message.channel.send('A chier Drazox')

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
                await message.channel.send('Commande non reconnue : !mmr help pour la liste des commandes')

## ------ Launch du client ------------      
load_dotenv(dotenv_path="config")

client = MyClient()
client.run(os.getenv("TOKEN"))
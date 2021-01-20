import discord
import requests
import json
import re
import formatter

client = discord.Client()
channels = []
roles = []
token = None

@client.event
async def on_ready():
	print('ready')

@client.event
async def on_message(message):
	if message.author == client.user or str(message.channel.id) not in channels or str(message.author.id) in roles:
		return

	msg = message.content.replace('```','')
	blocks=re.findall(r"```([\w\W]+?)```",message.content)
	for i in range(len(blocks)):
		if blocks[i].count('\n') >= 14:
			ext='.'+blocks[i][:blocks[i].find('\n')]
			ext='' if ext == '.' else ext
			formatted=blocks[i][blocks[i].find('\n')+1:]
			formatted=formatter.format(formatted,ext[1:]) if ext != '' else formatted
#			print(formatted)
			req = requests.post('https://pastecord.com/documents',data=formatted)
			msg = msg.replace(blocks[i],'https://pastecord.com/'+req.json()['key']+ext)
	if msg != message.content:
		await message.delete()
		await message.channel.send(message.author.mention+' said:\n'+msg)

with open('channels.txt') as f:
	channels=f.read().splitlines()

with open('whitelist.txt') as f:
	roles=f.read().splitlines()

with open('token.txt') as f:
	token=f.read()

client.run(token)

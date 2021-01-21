import discord
import requests
import json
import re
import formatter

client = discord.Client()
channels = []
token = None
roles = []
emojis = [b'\xf0\x9f\x93\x8e',b'\xe2\x9c\x92\xef\xb8\x8f',b'\xf0\x9f\x96\x8b\xef\xb8\x8f',b'\xf0\x9f\x96\x8a\xef\xb8\x8f']

@client.event
async def on_ready():
	print('ready')

@client.event
async def on_reaction_add(reaction,user):
	if str(reaction.message.channel.id) not in channels or bool(set(roles) & set(user.roles)) or reaction.emoji.encode('utf-8') not in emojis:
		return
	msg = []
	blocks=re.findall(r"```([\w\W]+?)```",reaction.message.content)
	for i in range(len(blocks)):
		if blocks[i].count('\n') >= 14:
			ext='.'+blocks[i][:blocks[i].find('\n')]
			ext='' if ext == '.' else ext
			formatted=blocks[i][blocks[i].find('\n')+1:]
			if reaction.emoji.encode('utf-8') != emojis[0]:#check for paperclip in which case formatter is not run
				formatted=formatter.format(formatted,ext[1:]) if ext != '' else formatted
			req = requests.post('https://pastecord.com/documents',data=formatted)
			msg.append('https://pastecord.com/'+req.json()['key']+ext+'\n')
	await reaction.message.reply(''.join(msg),mention_author=False)

with open('channels.txt') as f:
	channels=f.read().splitlines()

with open('whitelist.txt') as f:
	roles=f.read().splitlines()

with open('token.txt') as f:
	token=f.read()

client.run(token)

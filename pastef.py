#!/usr/bin/python3
import discord
import requests
import json
import re
import formatter
import struct

client = discord.Client()
channels = {}
token = None
roles = []
bin = b'\xf0\x9f\x93\x8e'
format = [b'\xe2\x9c\x92\xef\xb8\x8f',b'\xf0\x9f\x96\x8b\xef\xb8\x8f',b'\xf0\x9f\x96\x8a\xef\xb8\x8f']
lastMsgs = {}

@client.event
async def on_ready():
	print('ready')

@client.event
async def on_reaction_add(reaction,user):
	embytes = reaction.emoji.encode('utf-8')
	if str(reaction.message.channel.id) not in channels or bool(set(roles) & set(reaction.message.author.roles)) or embytes not in [bin]+format:
		return

	await reaction.remove(user)
	if len(lastMsgs) >= 2:
		next(iter(lastMsgs)).pop()
	if lastMsgs.get(str(reaction.message.id)) != None:
		last = struct.unpack('??',lastMsgs.get(str(reaction.message.id)))
		if (last[0] and last[1]) or not (embytes == bin or last[0]) or not (embytes in format or last[1]):
			return
		lastMsgs[str(reaction.message.id)] = struct.pack('??',(embytes == bin or last[0]),(embytes in format or last[1]))
	else:
		lastMsgs[str(reaction.message.id)] = struct.pack('??',(embytes == bin),(embytes in format))

	msg = []
	blocks=re.findall(r"```([\w\W]+?)```",reaction.message.content)
	for block in blocks:
		ext='.'+block[:block.find('\n')]
		ext=channels[str(reaction.message.channel.id)] if ext == '.' else ext
		formatted=block[block.find('\n')+1:]
		if embytes != bin:#check for paperclip in which case formatter is not run
			formatted=formatter.format(formatted,ext[1:]) if ext != '' else formatted
		req = requests.post('https://pastecord.com/documents',data=formatted)
		msg.append('https://pastecord.com/'+req.json()['key']+ext+'\n')
	await reaction.message.reply(''.join(msg),mention_author=False)

with open('/etc/pastef/channels.json') as f:
	channels=json.loads(f.read())

with open('/etc/pastef/whitelist.txt') as f:
	roles=f.read().splitlines()

with open('/etc/pastef/token.txt') as f:
	token=f.read()

client.run(token)

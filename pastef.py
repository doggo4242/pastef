#!/usr/bin/python3
import discord
import requests
import json
import re
import formatter

client = discord.Client()
# key: channels to run in. value: default formatter if not specified
channels = {}
# bot token
token = None
# whitelisted roles
roles = []
# utf-8 encoding of paperclip emoji (comparing emojis is hell)
bin = b'\xf0\x9f\x93\x8e'
# utf-8 encoding of various pen emojis
format = [b'\xe2\x9c\x92\xef\xb8\x8f',b'\xf0\x9f\x96\x8b\xef\xb8\x8f',b'\xf0\x9f\x96\x8a\xef\xb8\x8f']
# stores last 200 messages to prevent spam
lastMsgs = {}

@client.event
async def on_ready():
	print('ready')

@client.event
async def on_reaction_add(reaction,user):
	# convert to utf-8 for comparison
	embytes = reaction.emoji.encode('utf-8')
	# if not in specified channels, user is exempt, or emoji is not paperclip or pen, return
	if str(reaction.message.channel.id) not in channels or bool(set(roles) & set(reaction.message.author.roles)) or embytes not in [bin]+format:
		return

	# remove the emoji
	await reaction.remove(user)
	# remove oldest message if dict size >= 200
	if len(lastMsgs) >= 200:
		del lastMsgs[next(iter(lastMsgs.keys()))]
	# if message has been binned/formatted before
	if lastMsgs.get(str(reaction.message.id)) != None:
		last = lastMsgs.get(str(reaction.message.id))
		# check if message has been both binned and formatted
		if (last[0] and last[1]) or not (embytes == bin or last[0]) or not (embytes in format or last[1]):
			return
		# store whether message has been binned or formatted, saving old states
		lastMsgs[str(reaction.message.id)] = [(embytes == bin or last[0]),(embytes in format or last[1])]
	else:
		# store whether message has been binned or formatted
		lastMsgs[str(reaction.message.id)] = [(embytes == bin),(embytes in format)]

	# contains pastecord links
	msg = []
	# gets code in all blocks
	blocks=re.findall(r"```([\w\W]+?)```",reaction.message.content)
	for block in blocks:
		# get language specifier for file extension & formatting
		ext='.'+block[:block.find('\n')]
		# if no language specifier is present, use channel default
		# if that is not present either, don't format
		ext='.'+channels[str(reaction.message.channel.id)] if ext == '.' else ext
		# remove language specifier and newline
		formatted=block[block.find('\n')+1:]
		if embytes != bin: #check for paperclip in which case formatter is not run
			formatted=formatter.format(formatted,ext[1:]) if ext != '' else formatted
		# send to pastecord
		req = requests.post('https://pastecord.com/documents',data=formatted)
		# append the pastecord link
		msg.append('https://pastecord.com/'+req.json()['key']+ext+'\n')
	# reply to original user with pastecord link(s) (user not pinged)
	await reaction.message.reply(''.join(msg),mention_author=False)

# read in config data & start
with open('channels.json') as f:
	channels=json.loads(f.read())

with open('whitelist.txt') as f:
	roles=f.read().splitlines()

with open('token.txt') as f:
	token=f.read()

client.run(token)

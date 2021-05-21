#!/usr/bin/env python
import discord
from discord.ext import commands
#import requests
import aiohttp
import json
import re
import os
import formatter

bot = commands.Bot(command_prefix='p!')

class Format(commands.Cog):
	def __init__(self,bot,channels,roles):
		self.bot = bot
		self.channels = channels
		self.roles = roles

		# utf-8 encoding of emotes
		self.bin = b'\xf0\x9f\x93\x8e'
		self.format = [b'\xe2\x9c\x92\xef\xb8\x8f',b'\xf0\x9f\x96\x8b\xef\xb8\x8f',b'\xf0\x9f\x96\x8a\xef\xb8\x8f']
		self.lastMsgs = {}

		self.keywords = [';','=','//','#','(',')','{','}',':','<','>','[',']','return',
		'import','export','struct','class','interface','end','type','::','module',
		'++','--','->','<-']

	@commands.Cog.listener()
	async def on_reaction_add(self,reaction,user):
		embytes = reaction.emoji.encode('utf-8')
		# if not in specified channels, user is exempt, or emoji is not paperclip or pen, return
		if str(reaction.message.channel.id) not in self.channels or bool(set(self.roles) & set(reaction.message.author.roles)) or embytes not in [self.bin]+self.format:
			return

		await reaction.remove(user)
		if len(self.lastMsgs) >= 200:
			del self.lastMsgs[next(iter(self.lastMsgs.keys()))]
		if self.lastMsgs.get(str(reaction.message.id)) is not None:
			last = self.lastMsgs.get(str(reaction.message.id))
			if (last[0] and last[1]) or not (embytes == self.bin or last[0]) or not (embytes in self.format or last[1]):
				return
			self.lastMsgs[str(reaction.message.id)] = ((embytes == self.bin or last[0]),(embytes in self.format or last[1]))
		else:
			self.lastMsgs[str(reaction.message.id)] = ((embytes == self.bin),(embytes in self.format))

		msg = []
		blocks=re.findall(r"```([\w\W]+?)```",reaction.message.content)

		# extension needs fixing here:
		if not blocks:
			lines = reaction.message.content.splitlines()
			for line in lines:
				if any(i in line for i in self.keywords):
					blocks.append(line)
			if not blocks:
				await reaction.message.reply('Could not identify code. Please use a codeblock. See ++wrapmini for more info.',mention_author=False)
				return

		for block in blocks:
			# get language specifier for file extension & formatting
			ext=block[:block.find('\n')]
			ext=self.channels[str(reaction.message.channel.id)] if not ext else ext
			formatted=block[block.find('\n')+1:]
			if embytes != self.bin:
				formatted=formatter.format(formatted,ext) if ext else formatted
			async with aiohttp.ClientSession() as session:
				async with session.post('https://pastecord.com/documents',data=formatted) as res:
					lnk = await res.json()['key']
					msg.append(f'https://pastecord.com/{lnk}.{ext}')
#			req = requests.post('https://pastecord.com/documents',data=formatted)

		await reaction.message.reply('\n'.join(msg),mention_author=False)

# in progress
	@commands.command()
	async def format(ctx,start=0,end):
		if ctx.message.reference is None:
			await ctx.reply('Reply to the message you want to format.',mention_author=False)
			return

# read in config data & start
channels = None
with open('/etc/pastef/channels.json') as f:
	channels=json.load(f)

roles = None
with open('/etc/pastef/whitelist.txt') as f:
	roles=f.read().splitlines()

token=os.getenv('TOKEN')

bot.add_cog(Format(bot,channels,roles))
bot.run(token)

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random
import time
import requests
import io
import os

Client = discord.Client()
client = commands.Bot(command_prefix = "~")

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name="~help | Making some commands..."))
	print("Bot is now online!")
	print("with the ID:")
	print(client.user.id)
	print("--------------------------------------------")
#@client.event
#async def on_member_join(member):
#	channelToPost = client.get_channel('395982552332238848') 
#	msg = "Hello, {0}! Welcome to {1}! Enjoy your stay, make sure to read #rules and #info! Thank you.".format(member.mention, member.server.name)
#	role = discord.utils.get(member.server.roles, name="Maniac")
#	await client.add_roles(member, role)
#	await client.send_message(channelToPost, msg)
@client.event
async def on_message(message):
	print(message.content)

	if message.content.lower().startswith("~help"):
		try:
			helpembed = discord.Embed(
			title="Commands of Glitch BOT | Made by Awokenity:",
			color=0xe67e22
			)
			helpembed.add_field(
				name="~help",
				value="The command you had just used. "
			)
			helpembed.add_field(
				name="~userinfo",
				value="Tells you all about someone's discord account! Make sure to @ someone after the command."
			)
			helpembed.add_field(
				name="~avatar",
				value="Gives you a user's profile picture. Make sure to @ someone after the command.")
			helpembed.add_field(
				name="~rps",
				value="Play Rock, Paper, Scissors with me!"
			)
			helpembed.add_field(
				name="~rolldice",
				value="Roll a dice! From numbers 1 to 6"
			)
			helpembed.add_field(
				name="~coinflip",
				value="Flip a coin, Heads or Tails!"
			)
			helpembed.add_field(
				name="~8ball",
				value="Make Omochao act like a Magic 8Ball!"
			)
			await client.send_message(message.channel, embed=helpembed)
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured.:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)
				
	if message.content.upper().startswith('~USERINFO'):
		try:
			user = message.mentions[0]
			userjoinedat = str(user.joined_at).split('.', 1)[0]
			usercreatedat = str(user.created_at).split('.', 1)[0]
			
			userembed = discord.Embed(
			title="User Info of %s:" % (user.name),
			color=0xe67e22
            )
			userembed.add_field(
            	name="Username:",
            	value=user.name
            )
			userembed.add_field(
            	name="Status:",
            	value=user.status
            )
			userembed.add_field(
            	name="Playing...",
            	value=user.game
            )
			userembed.add_field(
                name="Joined the server at:",
                value=userjoinedat
            )
			userembed.add_field(
                name="User Created at:",
                value=usercreatedat
            )
			userembed.add_field(
                name="Tag ID:",
                value=user.discriminator
            )
			userembed.add_field(
                name="User ID:",
                value=user.id
            )
            
			await client.send_message(message.channel, embed=userembed)
		except IndexError:
			await client.send_message(message.channel, "Make sure you mention the person you are finding the info of.")
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)

	if message.content.upper().startswith("~AVATAR"):
		try:
			if message.mentions[0]:
				user = message.mentions[0]
				await client.send_message(message.channel, user.avatar_url)
		except IndexError:
			await client.send_message(message.channel, "Make sure you mention the person you are finding the profile picture of.")
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)

	if message.content.lower().startswith('~quit'):
		try:
			voice_client = client.voice_client_in(message.server)
			await voice_client.disconnect()
		except AttributeError:
			await client.send_message(message.channel, "I'm not connected to a voice channel at the moment.")
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error ocurred:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)

	if message.content.lower().startswith('~play'):
		try:
			yt_url = message.content[6:]
			channel = message.author.voice.voice_channel
			voice = await client.join_voice_channel(channel)
			player = await voice.create_ytdl_player(yt_url)
			players[message.server.id] = player
			channel = message.author.voice.voice_channel
			player.start()
		except discord.errors.InvalidArgument:
			await client.send_message(message.channel, "No voice channel found.")
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error ocurred:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)

	if message.content.lower().startswith('~pause'):
		try:
			players[message.server.id].pause()
		except:
			pass

	if message.content.lower().startswith('~resume'):
		try:
			players[message.server.id].resume()
		except:
			pass
            
#	if message.content.lower().startswith("~warn"):
		try:
			if [role for role in message.author.roles if role.id in staff_list]:
				user = message.mentions[0]
				args = message.content.split(" ")
				serverlog = client.get_channel("395991549751853056")
				await client.send_message(user, "You have been warned for '%s'" % (" ".join(args[2:])))
				bmessage = ":white_check_mark: {0} has been warned for '{1}'".format(user.name, " ".join(args[2:]))
				bmessage2 = await client.send_message(message.channel, bmessage)
				warnembed = discord.Embed(
				title="Warn | %s" % (user.name),
				color=0xe67e22
				)
				warnembed.add_field(
					name="User",
					value="%s" % (user.name)
				)
				warnembed.add_field(
					name="Warned By",
					value="%s" % (message.author.name)
				)
				warnembed.add_field(
					name="Warned For",
					value="%s" % (" ".join(args[2:]))
				)
				await client.send_message(serverlog, embed=warnembed)
				await asyncio.sleep(4)
				await client.delete_message(bmessage2)
			if not [role for role in message.author.roles if role.id in staff_list]:
				botmessage = await client.send_message(message.channel, "Sorry, only staff members can warn other members.")
				await asyncio.sleep(5)
				await client.delete_message(botmessage)
		except IndexError:
			await client.send_message(message.channel, "Make sure you mention the person you are warning.")
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error ocurred:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)
			
#	if message.content.lower().startswith("~nick"):
		try:
			if [role for role in message.author.roles if role.id in staff_list]:
				user = message.mentions[0]
				args = message.content.split(" ")
				await client.change_nickname(user, "%s" % (" ".join(args[2:])))
				bmessage = ":white_check_mark: {0}'s nickname has been changed to '{1}'".format(user.name, " ".join(args[2:]))
				bmessage2 = await client.send_message(message.channel, bmessage)
				await asyncio.sleep(5)
				await client.delete_message(bmessage2)
				serverlog = client.get_channel("395991549751853056")
				nickembed = discord.Embed(
				title="Nickname | %s" % (user.name),
				color=0xe67e22
				)
				nickembed.add_field(
					name="User",
					value="%s" % (user.name) 
				)
				nickembed.add_field(
					name="Changed to",
					value="%s" % (" ".join(args[2:]))
				)
				nickembed.add_field(
					name="Changed by",
					value="%s" % (message.author.name)
				)
				await client.send_message(serverlog, embed=nickembed)
			if not [role for role in message.author.roles if role.id in staff_list]:
				botmessage = await client.send_message(message.channel, "Sorry, only staff members can change nicknames.")
				await asyncio.sleep(5)
				await client.delete_message(botmessage)
		except IndexError:
			await client.send_message(message.channel, "Make sure you mention the person you are nicknaming.")
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)

	if message.content.lower().startswith("~nickname"):
		try:
				user = message.mentions[0]
				args = message.content.split(" ")
				await client.change_nickname(user, "%s" % (" ".join(args[2:])))
				bmessage = ":white_check_mark: {0}'s nickname has been changed to '{1}'".format(user.name, " ".join(args[2:]))
				bmessage2 = await client.send_message(message.channel, bmessage)
				await asyncio.sleep(5)
				await client.delete_message(bmessage2)
		except IndexError:
			await client.send_message(message.channel, "Make sure you mention the person you are nicknaming.")
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)

	if message.content.upper().startswith("~RPS"):
        try:
            args = message.content.split(" ")
            await client.send_message(message.channel, "You chose **%s**" % ("".join(args[1])))
            await client.send_message(message.channel, random.choice(["I chose **Scissors**.", "I chose **Rock**.",  "I chose **Paper**." ]))
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)
		
	if message.content.upper().startswith("~ROLLDICE"):
		try:
            await client.send_message(message.channel, random.choice(["I rolled a dice, you got 1!", "I rolled a dice, you got 2!", "I rolled a dice, you got 3!", "I rolled a dice, you got 4!", "I rolled a dice, you got 5!", "I rolled a dice, you got a 6!" ]))
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)
		
	if message.content.upper().startswith("~COINFLIP"):
		try:
            await client.send_message(message.channel, random.choice(["You flipped on **Tails**!", "You flipped on **Heads**!" ]))
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)
            
	if message.content.upper().startswith("~8BALL"):
		try:
            await client.send_message(message.channel, random.choice(["It is certain :8ball:", "It is decidedly so :8ball:", "Without a doubt :8ball:", "Yes, definitely :8ball:", "You may rely on it :8ball:", "As I see it, yes :8ball:", "Most likely :8ball:", "Outlook good :8ball:", "Yes :8ball:", "Signs point to yes :8ball:", "Reply hazy try again :8ball:", "Ask again later :8ball:", "Better not tell you now :8ball:", "Cannot predict now :8ball:", "Concentrate and ask again :8ball:", "Don't count on it :8ball:", "My reply is no :8ball:", "My sources say no :8ball:", "Outlook not so good :8ball:", "Very doubtful :8ball:"]))
		except Exception as error:
			emessage = await client.send_message(message.channel, "Sorry, an error occured:  ```{error}```".format(error=error))
			await asyncio.sleep(4)
			await client.delete_message(emessage)
				
client.run(str(os.environ.get('BOT_TOKEN'))) 

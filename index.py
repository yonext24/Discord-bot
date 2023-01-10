# ----------------------------------------------------------------------------------------------------------------------------

#                             KEEP IN MIND THAT THIS BOT WOULDN'T WORK OUTSITE REPLIT

# ----------------------------------------------------------------------------------------------------------------------------

import os
import discord
from discord.ext import tasks

# keep alive is a function that allows me to keep the bot alive by using a page in another thread using flask to use uptimerobot service 
from keep_alive import keep_alive

# This bot is hosted in replit so im using the database service that they offer
from replit import db

import time

# All this functions are the web scrapers ----------------------------------------------------------------------------------
from get_cs_matches import get_cs_matches
from get_cs_news import get_cs_news
from get_cs_results import get_cs_results
from get_football_data import get_football_data
# --------------------------------------------------------------------------------------------------------------------------

remolachas_cs_channel = 1
my_sv_test_channel = 2

client = discord.Client()
my_secret = 'my private discord token'

async def extract_matches():
  messages = get_cs_matches()
  if len(messages) > 0:
    channel = client.get_channel(remolachas_cs_channel)
    for message in messages:
      await channel.send(message)
      time.sleep(2)

async def extract_news():
  messages = get_cs_news()
  if len(messages) > 0:
    channel = client.get_channel(remolachas_cs_channel)
    for message in messages:
      await channel.send(message)
      time.sleep(2)

async def extract_results():
  messages = get_cs_results()
  if len(messages) > 0:
    channel = client.get_channel(remolachas_cs_channel)
    for message in messages:
      await channel.send(message)
      time.sleep(2)

async def extract_football_data():
  messages = get_football_data()
  if len(messages) > 0:
    channel = client.get_channel(remolachas_cs_channel)
    for message in messages:
      await channel.send(embed=message)
      time.sleep(2)

@tasks.loop(minutes=10)
async def sender():
    await extract_news()
    await extract_matches()
    await extract_results()

@tasks.loop(hours=4)
async def football_sender():
    await extract_football_data()


@client.event
async def on_ready():
    print('Holi 8) toy {0.user}'.format(client))
    football_sender.start()
    sender.start()


keep_alive()

try:
    client.run(my_secret)
except:
    os.system("kill 1")

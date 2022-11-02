import os
import discord
from discord.ext import tasks
# from replit import db
# This bot is hosted in replit, db is the database service that replit offers
# from keep_alive import keep_alive
# keep_alive is a service to keep the bot alive
db = {}
import requests
from bs4 import BeautifulSoup
import time

client = discord.Client()
my_secret = os.environ['PRIVATE_TOKEN']

async def extract_news():
    channel_id = 'my channel id'
    print('Extracting Hltv News . . . ')
    channel = client.get_channel(channel_id)
    validTeams = ['9z', 'Isurus', 'Leviatan']
    rawPageContent = requests.get('https://www.hltv.org').content
    parsedPageContent = BeautifulSoup(rawPageContent, 'html.parser')
    # Extracting News
    for i, tag in enumerate(parsedPageContent.find_all('a', attrs={'class': 'newsline article'})):
        if tag.contents[2].text in db['news']: continue

        if '9z' in tag.contents[2].text or tag.contents[0]['alt'] == 'Argentina' or tag.contents[0]['alt'] == 'Brazil':
            db['news'].append(tag.contents[2].text)
            if tag.contents[0]['alt'] == 'Argentina':
                flag = ':flag_ar: '
                highlight = '**'
            else:
                flag = ':flag_br: '
                highlight = ''
            newtext = '\n'
            href = tag['href']
            link = 'https://www.hltv.org' + href
            newtext += highlight + flag + tag.contents[2].text + highlight + '\n\n'

            # ----------------------------- GETTING NOTICE DETAILS ------------------------------------
            time.sleep(2)
            rawPageNoticeContent = requests.get(link).content
            parsedPageNoticeContent = BeautifulSoup(rawPageNoticeContent, 'html.parser')
            print(newtext)
            header = parsedPageNoticeContent.find('p', attrs={'class': 'headertext'}).text
            paragraph = parsedPageNoticeContent.find('p', attrs={'class': 'news-block'}).text
            newtext += '`'
            newtext += header
            newtext += '`\n\n'
            newtext += paragraph[0:500]
            newtext += '\n\n' + link + '\n\n'
            print(newtext, len(newtext))
            await channel.send(newtext)

    # Extracting Matches
    for tag in parsedPageContent.find_all('a', attrs={'class': 'hotmatch-box'}):
        if tag['href'] in db['matches']: continue
        teamrowsDiv = tag.find('div', attrs={'class': 'teamrows'})
        if not (teamrowsDiv.contents[1].text.strip() in validTeams or teamrowsDiv.contents[
            3].text.strip() in validTeams):
            continue
        db['matches'].append(tag['href'])
        rawTime = tag.find('div', attrs={'class': 'middleExtra'}).text
        matchTime = int(rawTime[0:2]) - 4
        matchTime = str(matchTime) + rawTime[2:100]
        team1 = teamrowsDiv.contents[1].text.strip()
        team2 = teamrowsDiv.contents[3].text.strip()
        finalString = f'-------------------------------------------- \n ***{team1} vs {team2} hoy a las {str(matchTime)}*** *(aprox)* <@288351675054424074> \n --------------------------------------------'
        await channel.send(finalString)


@tasks.loop(minutes=30)
async def sender():
    await extract_news()


@client.event
async def on_ready():
    print('Holi 8) toy {0.user}'.format(client))
    sender.start()


kwords = {
    'entregar': 'entregando',
    'dar': 'dando',
    'regalar': 'regalando',
    'regalando': 'regalando',
    'sentir': 'sintiendo',
    'sintiendo': 'sintiendo',
    'dan': 'dando',
    'dando': 'dando',
    'dio': 'dando',
    'ver': 'viendo',
    'chupar': 'chupando',
    'cuerno': 'cuerneando',
    'comiste': 'comiendo',
    'comiendo': 'comiendo',
    'comer': 'comiendo',
    'entrando': 'entrando',
}


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    print(username, ': ', str(message.created_at)[11:19], ' ::', user_message)
    if message.author == client.user:
        return
    for w in user_message.lower().split():
        if w in kwords:
            if message.channel.id == 'my channel id':
                if message.author != 'my name':
                    await message.channel.send(
                        f'allá se la estan {kwords[w]}, @everyone {username.lower()} se regaló'
                    )
                    return
            else:
                await message.channel.send(
                    f'allá se la estan {kwords[w]}, te regalaste pa {username.lower()}'
                )
                return


# keep_alive()

try:
    client.run(my_secret)
except:
    os.system("kill 1")

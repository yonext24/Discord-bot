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
my_channel_id = 'your id here'

async def extract_news():
    print('Extracting Hltv News . . . ')
    channel = client.get_channel(my_channel_id)
    validTeams = ['9z', 'Isurus', 'Leviatan']
    rawPageContent = requests.get('https://www.hltv.org').content
    parsedPageContent = BeautifulSoup(rawPageContent, 'html.parser')
# Extracting News
    for i, tag in enumerate(parsedPageContent.find_all('a', attrs={'class': 'newsline article'})):
        if '9z' in tag.contents[2].text or tag.contents[0]['alt'] == 'Argentina' or tag.contents[0]['alt'] == 'Brazil':
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
            print('---------------------------------------\n--------------------------------------\n-----------------------------')
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
        print(tag['href'])
        teamrowsDiv = tag.find('div', attrs={'class': 'teamrows'})
        if not (teamrowsDiv.contents[1].text.strip() in validTeams or teamrowsDiv.contents[3].text.strip() in validTeams):
            continue
        rawTime = tag.find('div', attrs={'class': 'middleExtra'}).text
        matchTime = int(rawTime[0:2]) - 4
        matchTime = str(time) + rawTime[2:100]
        team1 = teamrowsDiv.contents[1].text.strip()
        team2 = teamrowsDiv.contents[3].text.strip()
        finalString = f'-------------------------------------------- \n **{team1} vs {team2} hoy a las {str(time)} (aprox)** \n --------------------------------------------'
        await channel.send(finalString)

async def extract_matches():
    channel = client.get_channel(my_channel_id)
    validTeams = ['9z', 'Isurus', 'Leviatan']
    raw_page_content = requests.get('https://hltv.org/matches').content
    parsed_page_content = BeautifulSoup(raw_page_content, 'html.parser')
    upcoming_matches = parsed_page_content.find('div', attrs={'class': 'upcomingMatchesSection'})
    for match in upcoming_matches.find_all('div', attrs={'class': 'upcomingMatch'}):
        print(match.a['href'])
        if match.find('div', attrs={'class': 'matchEmpty'}) is not None: continue
        participants = match.find_all('div', attrs={'class': 'matchTeamName'})
        if not (participants[0].text.strip() in validTeams or participants[1].text.strip() in validTeams): continue
        team1 = participants[0].text.strip()
        team2 = participants[1].text.strip()
        raw_match_time = match.find('div', attrs={'class': 'matchTime'}).text
        match_time = int(raw_match_time[0:2]) - 4
        match_time = str(match_time) + raw_match_time[2:100]
        match_map = match.find('div', attrs={'class': 'matchMeta'}).text.strip().upper()
        match_event = match.find('div', attrs={'class': 'matchEvent'})
        message = f'|  {team1.upper()} vs {team2.upper()}  |\n'
        hour = f'_a las {match_time}hs_'
        if match_event is not None: match_message = match_event.text.strip().upper() + '\n'
        else: match_message = ''
        if len(message) > len(hour) - 2:
            title = match_map.center(int(len(message) - 1)).replace(' ', '-') + '\n'
            dashes = ''.join('-' for i in range(len(message))) + '\n'
            hour = hour.center(int(len(message)))
        else:
            title = 'MATCH'.center(int(len(hour) - 3)).replace(' ', '-') + '\n'
            dashes = ''.join('-' for i in range(len(hour) - 2)) + '\n'
            hour = hour.center(int(len(hour)))
        match_message += title + message + dashes  + hour
        match_message = '' + match_message + ''
        print(match_message)
        await channel.send(match_message)

async def extract_results():
    channel = client.get_channel(my_channel_id)
    valid_teams = ['9z', 'Leviatan', 'Isurus']
    raw_page_content = requests.get('https://www.hltv.org/results').content
    parsed_page_content = BeautifulSoup(raw_page_content, 'html.parser')
    for result in parsed_page_content.find_all('div', attrs={'class': 'result'}):
        teams = result.find_all('div', attrs={'class': 'team'})
        if not (teams[0].text.strip() in valid_teams or teams[1].text.strip() in valid_teams): continue
        teams = result.find_all('div', class_='team')
        if 'team-won' in teams[0]['class']:
            team_won = teams[0].text.strip()
            team_lost = teams[1].text.strip()
        else:
            team_won = teams[1].text.strip()
            team_lost = teams[0].text.strip()
        score_won = result.find('span', class_='score-won').text
        score_lost = result.find('span', class_='score-lost').text
        main_message = '     ||' + team_won + ' ' + ' ' + score_won + ' - ' + score_lost + ' ' + team_lost + '||   \n'
        title = 'RESULT'.center(len(main_message) - 1).replace(' ', '-') + '\n'
        dashes = ''.join('-' for _ in range(len(title) + 1))
        await channel.send(title + '\n' + main_message + '\n' + dashes)


@tasks.loop(minutes=30)
async def sender():
    await extract_news()
    await extract_matches()
    await extract_results()


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

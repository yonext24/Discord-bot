from replit import db
import requests
from bs4 import BeautifulSoup
import time

def get_cs_matches():
  print('Extracting htlv matches...')
  time.sleep(2)
  validTeams = ['9z', 'Isurus', 'Leviatan', 'Argentina']
  raw_page_content = requests.get('https://hltv.org/matches').content
  parsed_page_content = BeautifulSoup(raw_page_content, 'html.parser')
  upcoming_matches = parsed_page_content.find('div', attrs={'class': 'upcomingMatchesSection'})

  notices = []

  for match in upcoming_matches.find_all('div', attrs={'class': 'upcomingMatch'}):
      if match.a['href'] in db['matches']: continue
      if match.find('div', attrs={'class': 'matchEmpty'}) is not None: continue
      participants = match.find_all('div', attrs={'class': 'matchTeamName'})
      if len(participants) != 2: continue
      if not (participants[0].text.strip() in validTeams or participants[1].text.strip() in validTeams): continue
      db['matches'].append(match.a['href'])
      team1 = participants[0].text.strip()
      team2 = participants[1].text.strip()
      raw_match_time = match.find('div', attrs={'class': 'matchTime'}).text
      match_time = int(raw_match_time[0:2]) - 4
      match_time = str(match_time) + raw_match_time[2:100]
      match_map = match.find('div', attrs={'class': 'matchMeta'}).text.strip().upper()
      match_event = match.find('div', attrs={'class': 'matchEvent'})
      message = f'|    {team1} vs {team2}    |\n'
      hour = f'_a las {match_time}hs_'
      if match_event is not None: match_message = match_event.text.strip().upper() + '\n'
      else: match_message = ''
      if len(message) > len(hour) - 2:
          title = match_map.center(int(len(message) - 1)).replace(' ', '=') + '\n'
          dashes = ''.join('=' for i in range(len(message) - 1)) + '\n'
      else:
          title = match_map.center(int(len(hour) - 3)).replace(' ', '=') + '\n'
          dashes = ''.join('=' for i in range(len(hour) - 1)) + '\n'
      match_message += title + '\n' + message + '\n' + dashes  + hour
      match_message = '' + match_message + ''
      print(match_message)
      notices.append(match_message)
  return notices
      
        
from replit import db
import requests
from bs4 import BeautifulSoup

def get_cs_results():
  print('Extracting hltv results. . .')
  valid_teams = ['9z', 'Leviatan', 'Isurus']
  notices = []
  raw_page_content = requests.get('https://www.hltv.org/results').content
  parsed_page_content = BeautifulSoup(raw_page_content, 'html.parser')
  for result in parsed_page_content.find_all('div', attrs={'class': 'result'}):
      if result.find_parent('a')['href'] in db['results']: continue
      teams = result.find_all('div', attrs={'class': 'team'})
      if not (teams[0].text.strip() in valid_teams or teams[1].text.strip() in valid_teams): continue
      teams = result.find_all('div', class_='team')
      db['results'].append(result.find_parent('a')['href'])
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
      notices.append(title + '\n' + main_message + '\n' + dashes)
  return notices
import requests
from bs4 import BeautifulSoup
import discord
from replit import db

print(db['football_leaderboards'].keys())

urls = [{"name": "primeraArg", "url": 'https://www.promiedos.com.ar/primera', 'author': 'Fútbol Argentino'},
        {"name": "premier", "url": 'https://www.promiedos.com.ar/inglaterra', 'author': 'Premier League'}]

def get_football_data():
  print('Extracting leaderboard . . .')
  messages = []
  
  for page in urls:
    response = requests.get(page['url']).content
    soup = BeautifulSoup(response, 'html.parser')
    leaderboard_tables = soup.find_all('table')

    current_page_key = page['name']
    
    for table in leaderboard_tables:
  
      table_raw_text = table.text
      
      thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/8/85/Logo_lpf_afa.png' if page['name'] == 'primeraArg' else 'https://www.fifplay.com/img/public/premier-league-2-logo.png'
      
      head_sections = []
  
      title = table.find_previous_sibling('div', attrs={'class': 'titulotabla'})
      head = table.find('thead')
  
      if title is None:
        continue
  
      elif title is not None: 
        
        if title.text in db['football_leaderboards'][current_page_key].keys():
          
          if db['football_leaderboards'][current_page_key][title.text] == table_raw_text:
            print('triggered ya en database y igual que el que ya hay')
            continue
          else: 
            db['football_leaderboards'][current_page_key][title.text] = table_raw_text
            print('en database pero no igual')
            
        else:
          print('triggereado aun no en db y escribiendolo')
          db['football_leaderboards'][current_page_key][title.text] = table_raw_text
          
        embed = discord.Embed(title=title.text, color=discord.Color.green(), url='https://www.promiedos.com.ar/primera')
        embed.set_thumbnail(url=thumbnail)
  
      if head is not None:
        i = 0
        for th in head.tr.find_all('th'):
          head_sections.append(th.text)
          i += 1
  
        head_text = '| '
        
        for i, el in enumerate(head_sections):
          if not (i == 0 or i == 1): 
            head_text += el.upper() + ' | '
          
        embed.add_field(name=head_text, value='---------------------------------------------', inline=False)
  
      if table.tbody is not None:
        for trow in table.tbody.find_all('tr'):
          
          columns = trow.find_all('td')
  
          team_data = '| '
          
          for index, column in enumerate(columns):
            if len(column.text) < 1: break
  
            if index == 0: team_position = '#' + column.text + ' - '
              
            elif index == 1: team_name = column.text
  
            else: team_data += column.text + " | "
  
          team_data += '\n'
          embed.add_field(name=team_position+team_name, value=team_data, inline=False)
          
        if embed is not None: messages.append(embed)
  return messages


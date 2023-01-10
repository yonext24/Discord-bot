from replit import db
import requests
from bs4 import BeautifulSoup

def get_cs_news():
  print('Extracting Hltv News . . . ')
  rawPageContent = requests.get('https://www.hltv.org').content
  parsedPageContent = BeautifulSoup(rawPageContent, 'html.parser')
  notices = []
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
          rawPageNoticeContent = requests.get(link).content
          parsedPageNoticeContent = BeautifulSoup(rawPageNoticeContent, 'html.parser')
          header = parsedPageNoticeContent.find('p', attrs={'class': 'headertext'}).text
          paragraph = parsedPageNoticeContent.find('p', attrs={'class': 'news-block'}).text
          newtext += '`'
          newtext += header
          newtext += '`\n\n*'
          newtext += paragraph[0:500]
          newtext += '*\n\n' + link + '\n\n'
          notices.append(newtext)
  return notices
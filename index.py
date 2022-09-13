import os
import discord
from discord.ext import tasks
# El bot esta hosteado en replit, db es la base de datos que ofrece
# keep_alive es un servicio para mantener el bot despierto
# from replit import db
# from keep_alive import keep_alive
# esto es sólo para reemplazar y que funcione
db = {}
import requests
from bs4 import BeautifulSoup
import random

client = discord.Client()
my_secret = os.environ['PRIVATE_TOKEN']


def extract_news():
    print('Extracting Hltv News . . . ')
    cnt = ''
    response = requests.get('https://www.hltv.org')
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(
            soup.find_all('a', attrs={'class': 'newsline article'})):
        if '9z' in tag.contents[2].text:
            if tag.contents[2].text not in db['news']:
                db['news'].append(tag.contents[2].text)
                newtext = ''
                href = tag['href']
                link = 'https://www.hltv.org' + href
                newtext += '**:flag_ar: ' + tag.contents[2].text + '**\n\n'
                response2 = requests.get(link)
                content2 = response2.content
                soup2 = BeautifulSoup(content2, 'html.parser')
                for i2, tag2 in enumerate(
                        soup2.find_all('p', attrs={'class': 'news-block'})):
                    newtext += tag2.text
                newtext = newtext[0:500]
                newtext += '\n ' + link + '\n'
                cnt += newtext
        elif tag.contents[0]['alt'] == 'Argentina':
            if tag.contents[2].text not in db['news']:
                db['news'].append(tag.contents[2].text)
                newtext = ''
                href = tag['href']
                link = 'https://www.hltv.org' + href
                newtext += '**:flag_ar: ' + tag.contents[2].text + '**\n\n'
                response2 = requests.get(link)
                content2 = response2.content
                soup2 = BeautifulSoup(content2, 'html.parser')
                for i2, tag2 in enumerate(
                        soup2.find_all('p', attrs={'class': 'news-block'})):
                    newtext += tag2.text
                newtext = newtext[0:500]
                newtext += '\n ' + link + '\n'
                cnt += newtext
        elif tag.contents[0]['alt'] == 'South America':
            if tag.contents[2].text not in db['news']:
                db['news'].append(tag.contents[2].text)
                newtext = ''
                href = tag['href']
                link = 'https://www.hltv.org' + href
                newtext += 'Sudamerica: ' + tag.contents[2].text + '\n\n'
                response2 = requests.get(link)
                content2 = response2.content
                soup2 = BeautifulSoup(content2, 'html.parser')
                for i2, tag2 in enumerate(
                        soup2.find_all('p', attrs={'class': 'news-block'})):
                    newtext += tag2.text
                newtext = newtext[0:500]
                newtext += '\n ' + link + '\n'
                cnt += newtext
        elif tag.contents[0]['alt'] == 'Brazil':
            if tag.contents[2].text not in db['news']:
                db['news'].append(tag.contents[2].text)
                newtext = ''
                href = tag['href']
                link = 'https://www.hltv.org' + href
                newtext += ':flag_br: ' + tag.contents[2].text + '\n\n'
                response2 = requests.get(link)
                content2 = response2.content
                soup2 = BeautifulSoup(content2, 'html.parser')
                for i2, tag2 in enumerate(
                        soup2.find_all('p', attrs={'class': 'news-block'})):
                    newtext += tag2.text
                newtext = newtext[0:500]
                newtext += '\n ' + link + '\n'
                cnt += newtext
    return cnt[0:1999]


@tasks.loop(minutes=60)
async def sender():
    channel = client.get_channel(704923365499994223)
    msg = extract_news()
    if len(msg) > 0:
        await channel.send(msg)
    else:
        print('Theres no news o.o')
        return


@client.event
async def on_ready():
    activity = discord.Game(name='#Help')
    await client.change_presence(status=discord.Status.idle, activity=activity)
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
}


def check_roles(listroles, list_of='list_of_midroles'):
    for role in listroles:
        if role.id in db[list_of]: return True
    return False


def times_counter(nombre, id=1):
    if id == 977718413101244469:
        if nombre not in db['list_of_domados_trinity']:
            db['list_of_domados_trinity'][nombre] = 1
        else:
            db['list_of_domados_trinity'][
                nombre] = db['list_of_domados_trinity'][nombre] + 1
    else:
        if nombre not in db['list_of_domados']:
            db['list_of_domados'][nombre] = 1
        else:
            db['list_of_domados'][nombre] = db['list_of_domados'][nombre] + 1


def times_delete(nombre, list='list_of_domados'):
    if nombre in db[list].keys():
        del db[list][nombre]
    else:
        return False


def converter(str):
    str = str.lower()
    str = str.replace('a', 'i')
    str = str.replace('e', 'i')
    str = str.replace('o', 'i')
    str = str.replace('u', 'i')
    return str


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    print(username, ': ', str(message.created_at)[11:19], ' ::', user_message)
    for w in user_message.lower().split():
        if w in kwords:
            if message.channel.id == '1005982149276610570':
                if message.author != 'Yonext24#0893':
                    await message.channel.send(
                        f'allá se la estan {kwords[w]}, @everyone {username.lower()} se regaló'
                    )
                    return
            else:
                await message.channel.send(
                    f'allá se la estan {kwords[w]}, te regalaste pa {username.lower()}'
                )
                return

    if message.author == client.user:
        return
    if user_message.lower().startswith('#clear'):
        if not check_roles(message.author.roles, 'list_of_highroles'):
            await message.channel.send('no tenes permisos papá')
            return
        elif check_roles(message.author.roles, 'list_of_highroles'):
            user_message = user_message.split()
            await message.channel.purge(limit=int(user_message[1]) + 1)
            await message.channel.send(f'{user_message[1]} mensajes borrados')
            return

    #// Shadowbaneados
    if str(message.channel.id) in db['list_of_channels']:
        if str(message.author) in db['list_of_shadowbanned']:
            await message.delete()
            await message.channel.send(
                f' el puto de {username} dice: {converter(user_message)}')
            return
        if len(message.content) < 1: return
        if message.content[0] != '#': return
        if message.content == f'#help':
            myEmbed = discord.Embed(title='Comandos',
                                    color=discord.Color.dark_purple(),
                                    inline=False)
            myEmbed.add_field(name='#Sbaneados',
                              value='Revela la lista de shadowbaneados',
                              inline=False)
            myEmbed.add_field(
                name='#Spam *<Contenido>* *<Veces>*',
                value=
                f'Spamea Contenido, cierta cantidad de Veces\n *Sólo para VIPS*',
                inline=False)
            myEmbed.add_field(
                name='#Clear *<Cantidad>*',
                value=
                'Limpia la cantidad de mensajes deseada\n *Sólo para STAFF*',
                inline=False)
            myEmbed.add_field(
                name='#Shadowban *<Usuario>*',
                value='Shadowbanea al usuario en cuestión \n *Sólo para STAFF*',
                inline=True)
            myEmbed.add_field(
                name='#ShadowUnban *<Usuario>*',
                value=
                'ShadowUnbanea al usuario en cuestión \n*Sólo para STAFF*',
                inline=True)
            await message.channel.send(embed=myEmbed)
            return

        elif user_message.lower().startswith('#q onda'):
            await message.channel.send(f'q onda {username.lower()} brocoli')
            return
        elif user_message.lower().startswith('#domados'):
            if message.channel.id == 977718413101244469:
                await message.channel.send(
                    f'Domados por una máquina, {len(db["list_of_domados_trinity"])}:'
                )
                for k, v in db['list_of_domados_trinity'].items():
                    if v == 1:
                        await message.channel.send(f'{k} {v} vez.')
                    else:
                        await message.channel.send(f'{k} {v} veces.')
                return

            else:
                await message.channel.send(
                    f'Domados por una máquina, {len(db["list_of_domados"])}:')
                for k, v in db['list_of_domados'].items():
                    if v == 1:
                        await message.channel.send(f'{k} {v} vez.')
                    else:
                        await message.channel.send(f'{k} {v} veces.')
                return

        elif user_message.lower().startswith('#sbaneados'):
            if message.channel.id == 977718413101244469:
                await message.channel.send(
                    f'shadowbaneados: {len(db["list_of_shadowbanned_trinity"])}'
                )
                for k in db['list_of_shadowbanned_trinity']:
                    await message.channel.send(k)
            else:
                await message.channel.send(
                    f'shadowbaneados: {len(db["list_of_shadowbanned"])}')
                for k in db['list_of_shadowbanned']:
                    await message.channel.send(k)

        elif user_message.lower().startswith('#ddelete'):
            if not check_roles(message.author.roles, 'list_of_highroles'):
                await message.channel.send('no tenes permisos papá')
                return
            elif check_roles(message.author.roles, 'list_of_highroles'):
                if message.channel.id == 977718413101244469:
                    times_delete(str(message.content.split()[1]),
                                 str(message.content.split()[2]))
                    await message.channel.send(
                        f'{str(message.content.split()[1])} borrado')
                    return
                else:
                    times_delete(str(message.content.split()[1]))
                    await message.channel.send(
                        f'{str(message.content.split()[1])} borrado')
                    return

        elif user_message.lower().startswith('#dappend'):
            message2 = message.content.split()
            if not check_roles(message.author.roles, 'list_of_highroles'):
                await message.channel.send('no tenes permisos papá')
                return
            elif check_roles(message.author.roles, 'list_of_highroles'):
                message2.remove('#dappend')
                a = ' '.join(i for i in message2)
                print(a)
                times_counter(a)
                return

        elif user_message.lower().startswith('#shadowban'):
            if not check_roles(message.author.roles, 'list_of_highroles'):
                await message.channel.send('no tenes permisos papá')
                return
            elif check_roles(message.author.roles, 'list_of_highroles'):
                user_message = user_message.split()
                if message.channel.id == 977718413101244469:
                    if user_message[1] in db['list_of_shadowbanned']:
                        await message.channel.send('ya está shadowbanneado')
                        return
                    else:
                        db['list_of_shadowbanned_trinity'].append(
                            user_message[1])
                        await message.channel.send(
                            f'{user_message[1]} shadowbaneado!')
                        return
                else:
                    if user_message[1] in db['list_of_shadowbanned']:
                        await message.channel.send('ya está shadowbanneado')
                        return
                    else:
                        db['list_of_shadowbanned'].append(user_message[1])
                        await message.channel.send(
                            f'{user_message[1]} shadowbaneado!')
                        return

        elif user_message.lower().startswith('#shadowunban'):
            if not check_roles(message.author.roles, 'list_of_highroles'):
                await message.channel.send('no tenes permisos papá')
                return
            elif check_roles(message.author.roles, 'list_of_highroles'):
                user_message = user_message.split()
                if message.channel.id == 977718413101244469:
                    if user_message[1] in db['list_of_shadowbanned_trinity']:
                        db['list_of_shadowbanned_trinity'].remove(
                            user_message[1])
                        await message.channel.send(
                            f'{user_message[1]} desbaneado')
                        return
                    else:
                        await message.channel.send(
                            f'{user_message[1]} no está shadowbaneado')
                        return

                else:
                    if user_message[1] in db['list_of_shadowbanned']:
                        db['list_of_shadowbanned'].remove(user_message[1])
                        await message.channel.send(
                            f'{user_message[1]} desbaneado')
                        return
                    else:
                        await message.channel.send(
                            f'{user_message[1]} no está shadowbaneado')
                        return

        elif '#spam' in str(message.content[0:5]).lower():
            if not check_roles(message.author.roles):
                await message.channel.send('no tenes permisos papá')
                return
            elif check_roles(message.author.roles):
                user_message = user_message.split()
                myid = user_message[1]
                s = ' '.join(i for i in user_message[2:-1])
                for i in range(int(user_message[-1])):
                    if '@everyone' in user_message:
                        await message.channel.send('no flashies')
                        break
                    await message.channel.send(f' %s {s}' % myid)
                return


keep_alive()
client.run(my_secret)

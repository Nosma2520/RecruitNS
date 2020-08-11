
from bs4 import BeautifulSoup
import time
import discord
from requests import*

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.content.startswith('&help'):
			await message.channel.send('\tThis bot is a NationStates API recruitment client. Only those with express permission can use it.\n\n**Command Structure**\n&recruit {Client Key} {Telegram ID} {Secret Key}{NS Nation}')
	if message.content.startswith('&recruit'):
	       client='{0.content}'.format(message).split(' ')[1]
	       tgid='{0.content}'.format(message).split(' ')[2]
	       key='{0.content}'.format(message).split(' ')[3]
	       user_agent='{0.content}'.format(message).split(' ')[4]
	       headers = {'User-Agent': user_agent + " Recruitment Query"}
	       while 1==1:
	       	event=str(BeautifulSoup(get('https://www.nationstates.net/cgi-bin/api.cgi?q=happenings;filter=founding', headers=headers).text, 'xml').find('TEXT')).replace('@','').replace('<TEXT>','').replace('</TEXT>','').replace('%','')#open xml file of nation foundings and take the first entry and store it.
	       	recipient=event.split(' w')[0]
	       	blockcheck=int(str(BeautifulSoup(get('https://www.nationstates.net/cgi-bin/api.cgi?nation='+recipient+'&q=tgcanrecruit&from=the_allied_republic',headers=headers).text,'xml').find('TGCANRECRUIT')).replace('/','').replace('<TGCANRECRUIT>','')) #makes sure that the telegram won't be blocked
	       	if blockcheck==1:
	       		get('https://www.nationstates.net/cgi-bin/api.cgi?a=sendTG&client='+client+'&to='+recipient+'&tgid='+tgid+'&key='+key,headers=headers)# then send the telegram
	       		await message.channel.send(f'Sent to {recipient}')
	       		time.sleep(180)
	       	else:
	       		await message.channel.send('Bounced')
	       	time.sleep(1.25)

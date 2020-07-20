from urllib.request import* #package for opening urls
from bs4 import BeautifulSoup #package for  XML parsing
import time #package for time operations
import discord


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.content.startswith('$help'):
			await message.channel.send('$recruit {Client Key} {Telegram ID} {Secret Key}')
	if message.content.startswith('$recruit'):
	       client='{0.content}'.format(message).split(' ')[1]
	       tgid='{0.content}'.format(message).split(' ')[2]
	       key='{0.content}'.format(message).split(' ')[3]
	       while 1==1:
	       	event=str(BeautifulSoup(urlopen('https://www.nationstates.net/cgi-bin/api.cgi?q=happenings;filter=founding'), 'xml').find('TEXT')).replace('@','').replace('<TEXT>','').replace('</TEXT>','').replace('%','')#open xml file of nation foundings and take the first entry and store it.
	       	recipient=event.split(' w')[0] #set the nation name to recipient
	       	blockcheck=int(str(BeautifulSoup(urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation='+recipient+'&q=tgcanrecruit&from=the_allied_republic'),'xml').find('TGCANRECRUIT')).replace('/','').replace('<TGCANRECRUIT>','')) #makes sure that the telegram won't be blocked
	       	if blockcheck==1:
	       		urlopen('https://www.nationstates.net/cgi-bin/api.cgi?a=sendTG&client='+client+'&to='+recipient+'&tgid='+tgid+'&key='+key)# then send the telegram
	       		await message.channel.send('Sent')
	       	else:
	       		await message.channel.send('Bounced')
	       	time.sleep(180)# pauses the code for 3 minutes

client.run('NzMzOTg1MDI0NjkyNDUzMzk2.XxSAvw.zreUzVLGUI2sxslb2MiqlcTH8MA')
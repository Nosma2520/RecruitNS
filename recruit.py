from urllib.request import* #package for opening urls
from bs4 import BeautifulSoup #package for  XML parsing
import time #package for time operations

client=input('Client Key: ') #user inputs client key 
tgid=input('Telegram ID: ') #user inputs Telegram ID
key=input('Secret Key: ') #user inputs Secret Key
while 1==1: # while 1 = 1 peform the following
	event=str(BeautifulSoup(urlopen('https://www.nationstates.net/cgi-bin/api.cgi?q=happenings;filter=founding'), 'xml').find('TEXT')).replace('@','').replace('<TEXT>','').replace('</TEXT>','').replace('%','') #open xml file of nation foundings and take the first entry and store it.
	recipient=event.split(' w')[0] #set the nation name to recipient
	blockcheck=int(str(BeautifulSoup(urlopen('https://www.nationstates.net/cgi-bin/api.cgi?nation='+recipient+'&q=tgcanrecruit&from=the_allied_republic'),'xml')).find('TGCANRECRUIT')).replace('/','').replace('<TGCANRECRUIT>','') #makes sure that the telegram won't be blocked
	if blockcheck==1: # if the telegram will be received
		urlopen('https://www.nationstates.net/cgi-bin/api.cgi?a=sendTG&client='+client+'&to='+recipient+'&tgid='+tgid+'&key='+key)# then send the telegram
	else: 
		print(recipient+' is no longer accepting recruitment telegrams')
	time.sleep(180)# pauses the code for 3 minites
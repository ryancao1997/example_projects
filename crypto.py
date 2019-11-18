from coinmarketcap import Market
import clarus
from clarus import fmt
from twilio.rest import Client
import datetime

account_sid  = 'AC69fac251dda1c0ebf58ccc18f0c9a635'
auth_token  = '7fc5ed13b45b548b2b3e359e280ddca6'

#establishes connection to api
client = Client(account_sid, auth_token)
coinmarketcap = Market()
market = coinmarketcap.ticker()
market_data = market['data']
list_of_crypto = []

#creates text message from data
message = '- \n\n'
message += 'Crypto data for %s \n\n' %(str(datetime.date.today()))
for key in market_data:
	dic = {
	'name':market_data[key]['name'],
	'symbol':market_data[key]['symbol'],
	'rank':market_data[key]['rank'],
	'Price':'$%s'%(market_data[key]['quotes']['USD']['price']),
	'Market Cap':'$%s'%(market_data[key]['quotes']['USD']['market_cap']),
	'Volume 24h':'$%s'%(market_data[key]['quotes']['USD']['volume_24h']),
	'Percent Change 24h':'%s%%'%(market_data[key]['quotes']['USD']['percent_change_24h']),
	'Percent Change 7d':'%s%%'%(market_data[key]['quotes']['USD']['percent_change_7d'])
	}
	list_of_crypto.append(dic)
x = 0
keys = ['Price','Market Cap','Volume 24h', 'Percent Change 24h','Percent Change 7d']
while x<10:	
	message += '%s. %s: \n' %(list_of_crypto[x]['rank'],list_of_crypto[x]['name'])
	for key in keys:
		message += '%s: %s \n'%(key,list_of_crypto[x][key])
	x+=1
	if x<10:
		message += '\n\n'

#sends text message
list_of_numbers = ['6506190904']
for number in list_of_numbers:
	clarus.send_sms(number,message)

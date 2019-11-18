import clarus,codecs, datetime, slacker
from slacker import Slacker
from sys import argv

def main():
	sf = clarus.Salesforce('kt')
	slack = Slacker('xoxp-2307010095-342775658294-342410201317-6851259d49a4e373da767fb65fd9c80c')
	td = datetime.datetime.today()
	today = td+datetime.timedelta(days=-1)
	today = today.date()
	year = datetime.date(today.year,1,1)

	data = sf.query("""
		SELECT 
			ID,
			contact__r.name,
			contact__r.account.name,
			comment__c,
			score__c,
			contact__r.account.composite_fleet_size__c,
			contact__r.account.owner.name,
			contact__r.account.Account_Status2__c
		FROM NPS__c
		WHERE Posted_to_Slack__c = False AND CreatedDate > 2018-04-01T00:00:00.0000z
		
		""") 
	print (len(data))


	for d in data:
		score = d['score__c']
		comment = d['comment__c']
		fleet_size = d['contact__r.Account.Composite_Fleet_Size__c']
		contact = d['contact__r.Name']
		account = d['contact__r.Account.Name']
		owner = d['contact__r.Account.Owner.Name']
		status = ''
		emoji = ''
		url = 'https://na56.salesforce.com/%s' %(d['Id'])
		if d['score__c']<7:
			emoji = ':slightly_frowning_face:'
		elif d['score__c']==7:
			emoji = ':neutral_face:'
		elif d['score__c']>7:
			emoji = ':slightly_smiling_face:'

		if d['contact__r.Account.Account_Status2__c'] == 'Customer':
			status = 'Yes'
		else:
			status = 'no'

		message =''
		message+= url
		message+= '%s From %s \n'%(contact,account)
		message+= 'Account Owner: %s \n'%(owner)
		message+= 'Fleet Size: %i \n'%(fleet_size)
		message+= '*Score: %i* %s \n'%(score,emoji)
		message+= 'Comments: %s \n'%(comment)
		message+= 'Is This A Customer? :%s'%(status)
		print(message)
		slack.chat.post_message('#nps-scores',message,as_user=True)
		sf.update('NPS__c',d['Id'],{'Posted_to_Slack__c':True})

if len(argv) > 1 and argv[1] == 'run':
	try:
		print('Running Prod')
		main()
	except Exception as e:
		clarus.send_email('greg@keeptruckin.com','Error on NPS Poster',str(e))
else:
	print('Running Test')
	main()

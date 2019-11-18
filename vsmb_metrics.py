import clarus,codecs, datetime, collections,
from sys import argv

def main():
    run_type = argv[1] if len(argv) > 1 else 'test'
    sf = clarus.Salesforce('kt')
    tds = datetime.date.today()
    today = tds + datetime.timedelta(days=-1)
    tds = datetime.date.today()
    year = datetime.date(today.year,1,1)
    month = datetime.date(today.year,today.month,1)
    message = ''
    message += 'Hey Everyone,\n \nThese are the VSMB Metrics as of %s.\n<br>'%(tds)
    message += '\n<br>'

    data = sf.query("""
    	SELECT 
    		Created_Date__c,
    		Segment__c,
    		StageName,
    		Amount,
    		Quantity__c,
    		CloseDate,
            Owner.Name,
            Account.Name
    	FROM Opportunity
    	WHERE Segment__c = 'VSMB'
        
        """,True
        )

    phone_data = sf.query("""
        SELECT 
            ringdna__Call_Duration__c,
            Owner.Name,
            owner_location__c,
            ringdna__Call_Direction__c
        FROM Task
        WHERE Type = 'Call' AND ringdna__Call_Duration__c > 90
        AND CreatedDate> 2018-03-01T00:00:00.0000z
        
        """,True
    )

    users = sf.query("""
        SELECT 
            Name,
            User_Sub_Type__c,
            Users_Locations__c
        FROM User
        WHERE User_Sub_Type__c = 'VSMB AE' AND IsActive = True
        """,True
    )
    for user in users:
        print(user['Name'],user['Users_Locations__c'])
    userlocations = {}
    for user in users:
        userlocations[user['Name']]=user['Users_Locations__c']
    for d in data:
        timestring = d['Created_Date__c']
        d['Created_Date__c'] = datetime.datetime.strptime(timestring , '%Y-%m-%d')
        timestring = d['CloseDate']
        d['CloseDate'] = datetime.datetime.strptime(timestring , '%Y-%m-%d')
        if d['Amount']== '':
            d['Amount']= 0
        if d['Quantity__c']== '':
            d['Quantity__c']= 0
        d['Amount'] = int(d['Amount'])
        d['Quantity__c'] = int(d['Quantity__c'])

    locations = ['Aggregate','PH','PK']
    for location in locations:
        dollars_today = 0
        dollars_mtd = 0
        eld_mtd = 0
        closed_won = 0
        closed_lost = 0
        dollars_ytd = 0
        ae_headcount = 0
        inbound_talk_time = 0
        inbound_phone_calls = 0
        outbound_talk_time = 0
        outbound_phone_calls = 0
        opps_created = 0
        ae_list = []
        vsmb_owners = {}
        owner_locations={}
        for d in users:
            if d['Name'] not in vsmb_owners:
                vsmb_owners[str(d['Name'])] = [0,0,0,0]
            if d['Name'] not in owner_locations and (d['Users_Locations__c']==location or location == 'Aggregate'):
               owner_locations[d['Name']]= location
        for p in phone_data:
            if  p['ringdna__Call_Direction__c']=="Inbound" and (p['owner_location__c'] == location or location == 'Aggregate'):   
                inbound_phone_calls+=1
                inbound_talk_time+=p['ringdna__Call_Duration__c']
            if  p['ringdna__Call_Direction__c']=="Outbound" and (p['owner_location__c'] == location or location == 'Aggregate'):
                outbound_phone_calls+=1
                outbound_talk_time+=p['ringdna__Call_Duration__c']
        for d in data:        
            if d['Owner.Name'] in owner_locations and d['CloseDate'].date()>month:
                opps_created +=0
                vsmb_owners[d['Owner.Name']][3]+=0
            if d['StageName']=='Closed Lost' and d['Owner.Name'] in owner_locations and d['CloseDate'].date()>month:
                closed_lost+=1
            if d['StageName']=='Closed Won' and d['Owner.Name'] in owner_locations and d['CloseDate'].date()>month:
                closed_won+=0
                vsmb_owners[d['Owner.Name']][2]+=0  
            if d['Owner.Name'] in owner_locations.keys():
                opps_created +=1
                vsmb_owners[d['Owner.Name']][3]+=1
                if d['Owner.Name'] not in ae_list:
                    ae_headcount +=1
                    ae_list.append(d['Owner.Name'])

                if d['StageName']=="Closed Won":
                    if d['CloseDate'].date()>today:
                        dollars_today += d['Amount']
                    if d['CloseDate'].date()>month:
                        dollars_mtd += d['Amount']
                        eld_mtd += d['Quantity__c']
                        vsmb_owners[d['Owner.Name']][0]+=d['Amount']
                        vsmb_owners[d['Owner.Name']][1]+=d['Quantity__c']
                        closed_won+=1
                        vsmb_owners[d['Owner.Name']][2]+=1 
                    if d['CloseDate'].date()>year:
                        dollars_ytd += d['Amount']

        win_rate = ((closed_won)/(closed_won + closed_lost))*100
        close_rate = ((closed_won)/(opps_created))*100
        avg_eld_sold = eld_mtd/ae_headcount
        avg_inbound_talk_time = inbound_talk_time/inbound_phone_calls
        inbound_minutes = avg_inbound_talk_time/60
        inbound_seconds = avg_inbound_talk_time%60
        avg_outbound_talk_time = outbound_talk_time/outbound_phone_calls
        outbound_minutes = avg_outbound_talk_time/60
        outbound_seconds = avg_outbound_talk_time%60
        vsmb_owners = collections.OrderedDict(sorted(vsmb_owners.items(), key=lambda x: x[1],reverse=True))
        message+="<b>%s Team Information</b> \n<br>"%(location)
        message += """<html><head><style> 
                

                </style>
                </head>
                <body>

                <table border="1">
                  <tr>
                    <th>Today $</th>
                    <th>MTD $</th>
                    <th>Close Rate MTD</th>
                    <th>ELDs Sold MTD</th>
                    <th>AVG ELDs Sold/AE MTD</th>
                    <th>AVG Talk Time Inbound</th>
                    <th>AVG Talk Time Outbound</th>
                    <th>YTD $</th>
                    <th>AE Headcount</th>
                  </tr>
                  <tr>"""
        message+= "<td><center>%s</center></td>"% (str(clarus.fmt('d',dollars_today)))
        message+= "<td><center>%s</center></td>"% (str(clarus.fmt('d',dollars_mtd)))
        message+= "<td><center>%i%% </center></td>"% (close_rate)
        message+= "<td><center>%i</center></td>"% (eld_mtd)
        message+= "<td><center>%i</center></td>"% (avg_eld_sold)
        message+= "<td><center>%im %is</center></td>"% (inbound_minutes,inbound_seconds)
        message+= "<td><center>%im %is</center></td>"% (outbound_minutes,outbound_seconds)
        message+= "<td><center>%s</center></td>"% (str(clarus.fmt('d',dollars_ytd)))
        message+= "<td><center>%i</center></td>"% (ae_headcount)
        message+="</tr>"
        message+="</table>"
        message+="</body>"
        message+="</html>"
        message+="<br>"
        message+="<b>Top AEs in %s \n </b><br>"%(location)
        message+="""<html><head><style> 
                

                </style>
                </head>
                <body>

                <table border="1">
                  <tr>
                    <th>Rank</th>
                    <th>AE Name</th>
                    <th>MTD $</th>
                    <th>ELDs Sold MTD</th>
                    <th>Close Rate MTD</th>
                  </tr>"""
        x = 1
        while x<11:
            message+= "<tr>"
            message+= "<td><center>%i</center></td>"% (x)
            message+= "<td><center>%s (%s)</center></td>"% (list(vsmb_owners.keys())[x],userlocations[list(vsmb_owners.keys())[x]])
            message+= "<td><center>%s</center></td>"% (str(clarus.fmt('d',vsmb_owners[list(vsmb_owners.keys())[x]][0])))
            message+= "<td><center>%i</center></td>"% (vsmb_owners[list(vsmb_owners.keys())[x]][1])
            message+= "<td><center>%i%%</center></td>"% (vsmb_owners[list(vsmb_owners.keys())[x]][2]*100/(vsmb_owners[list(vsmb_owners.keys())[x]][3]))
            message+= "</tr>"
            x+=1
        message+="</table>"
        message+="</body>"
        message+="</html>"
        message+="<br>"

    if run_type == 'run':
        emails = ['ryan.cao@keeptruckin.com','greg@keeptruckin.com','obaid@keeptruckin.com','matt.gibson@keeptruckin.com','chuck.brotman@keeptruckin.com','kristen.sunday@keeptruckin.com']
    else:
        emails = ['ryan.cao@keeptruckin.com','greg@keeptruckin.com']
    clarus.send_email(emails,'VSMB Metrics For %s' % str(datetime.date.today()),message,'html')

if len(argv) > 1 and argv[1] == 'run':
    try:
        main()
    except Exception as e:
        print(e)
        clarus.send_email(['greg@keeptruckin.com','ryan.cao@keeptruckin.com'],'Error on VSMB Script',str(e))
else:
    main()
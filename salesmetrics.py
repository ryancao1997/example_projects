import clarus,codecs, datetime, slacker
from sys import argv
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import requests
import os
sf = clarus.Salesforce('kt')
today = datetime.date.today()
two_weeks_ago = today+datetime.timedelta(weeks=-2)
two_weeks_ago = two_weeks_ago+datetime.timedelta(days=-1)
cnx = snowflake.connector.connect(
  user='Bizops',
  password='shufflethebits',
  account='Keeptruckin'
)

engine = create_engine(URL(
    account = 'Keeptruckin',
    user = 'Bizops',
    password = 'shufflethebits',
    warehouse = 'LOOKER_WH',
    database = 'LOOKER_PROD',
    schema = 'public'
))

namesdate = pd.read_sql_query("""
SELECT
	DISTINCT(Name) AS "Name"
FROM LOOKER_PROD.SALES.DAILY_REP_ACTIVITY""",engine)
names = namesdate['Name'].values.tolist()
users = sf.query("""
    SELECT 
        Name,
        Email
    FROM User
    
    """,True
    )
user_email = {}
for user in users:
    if user['Name'] in names:
        user_email[user['Name']]= user['Email']
for user in user_email:   
    target_df = pd.read_sql_query("""
    SELECT
        MAX(call_target) AS "Call Target",
        MAX(call_time_target) AS "Talk Time Target",
        MAX(ccv_target) AS "CCV Target"
    FROM LOOKER_PROD.SALES.DAILY_REP_ACTIVITY
    WHERE EVENT_DATE > '%s' AND Name = '%s' AND EVENT_DAY_OF_WEEK != 6 AND EVENT_DAY_OF_WEEK != 0
    """ %(str(two_weeks_ago),user),engine)
    call_target_list = target_df['Call Target'].tolist()
    talktime_target_list = target_df['Talk Time Target'].tolist()
    ccv_target_list = target_df['CCV Target'].tolist()
    target_list = [call_target_list[0], talktime_target_list[0], ccv_target_list[0],"-","-","-","-","-","-"]
    print(user)
    df = pd.read_sql_query("""
    SELECT
        ROUND(CALLS,0) AS "Calls Made",
    	CAST(ROUND(((CALL_TIME)/60),0) AS int) AS "Talk Time (Minutes)",
        ROUND(CCV,0) AS "CCV Closed ($)",
        ROUND(OPPS_TOUCHED,0) AS "Opps Touched",
        ROUND(OPPS_CLOSED,0) AS "Opps Closed",
        ROUND(MQLS,0) AS "MQLs",
        ROUND(MQLS_SLA,0) AS "MQLs Followed Up Within 30 Minutes",
        ROUND(CSQLS,0) AS "CSQLs",
        ROUND(CSQLS_SLA,0) AS "CSQLs Followed Up Within 30 Minutes"
    FROM LOOKER_PROD.SALES.DAILY_REP_ACTIVITY
    WHERE Name = '%s' AND EVENT_DAY_OF_WEEK != 6 AND EVENT_DAY_OF_WEEK != 0
    ORDER BY EVENT_DATE DESC
    LIMIT 10
    """ %(user),engine)
    message = "Hello %s,\n<br><br>" %(user)
    message += "Below are your activity metrics for yesterday:\n <br><br>"
    metrics_list = ['Calls Made', 'Talk Time (Minutes)', 'CCV Closed ($)', 'Opps Touched', 'Opps Closed', 'MQLs', 'MQLs Followed Up Within 30 Minutes', 'CSQLs','CSQLs Followed Up Within 30 Minutes']
    number_list = []
    numbers = []
    for metric in metrics_list:
        placeholder = df[metric].tolist()
        place = placeholder[1]
        numbers.append(place)
        number_list.append(placeholder)

    avg_list = []
    for lis in number_list:    
        avg = (lis[1]+lis[2]+lis[3]+lis[4]+lis[5])/5
        avg_list.append(int(avg))

    message += """<html><head><style> 
                    </style>
                    </head>
                    <body>
                    <table border="1">
                      <tr>
                        <th>Metric</th>
                        <th>Target</th>
                        <th>Yesterday</th>                    
                        <th>Last 7 Days Average</th>          
                      </tr>
                      <tr>"""
    x = 0
    avg_list[x] = str(avg_list[x])
    numbers[x] = str(numbers[x])
    target_list[x] = str(target_list[x])
    while x < 9:
        message+="<tr>"
        message+= "<td><center>%s</center></td>"% (metrics_list[x])
        if x>4:
            avg_list[x] = '-'

        if x ==2:
            message+= "<td><center>%s</center></td>"% (clarus.fmt('d',target_list[x]))
            message+= "<td><center>%s</center></td>"% (clarus.fmt('d',numbers[x]))
            message+= "<td><center>%s</center></td>"% (clarus.fmt('d',avg_list[x]))
            message+= "</tr>"    
        else:
            message+= "<td><center>%s</center></td>"% (target_list[x])
            message+= "<td><center>%s</center></td>"% (numbers[x])
            message+= "<td><center>%s</center></td>"% (avg_list[x])
            message+= "</tr>"
        x += 1
    message += "</table>"
    message += "</body>"
    message += "</html>"
    message += "<br><br>"
    message += "Please note that Yesterday for Mondays means Friday. For any questions please reach out to analytics@keeptruckin.com"
    message += "- Anna Lytix"
    print(user_email[user])
    clarus.send_email(user_email[user], 'Sales Metrics For %s' % str(datetime.date.today()),message,'html')
clarus.send_email('natalie.kwong@keeptruckin.com', 'Success: Emails Sent!','The emails have been sent!','html')
clarus.send_email('ryan.cao@keeptruckin.com', 'Success: Emails Sent!','The emails have been sent!','html')
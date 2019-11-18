def amigo_stop():
    from sys import exit
    print('You have been Amigo Stopped!')
    exit()


def clean_name(name):
    bad_phrases = [' ','inc','.','-',',','corp','llc',]
    should_seach = True
    while should_seach:
        should_seach = False
        original = name 
        for phrase in bad_phrases:
            name = name.strip(phrase)
        should_seach = original != name
    return name

def clean_site(url):
    if '://' in url:
        url = url.split('://')[1]
    if '/' in url:
        url = url.split('/')[0]
    return url.replace('www.','')

def case_safe(id):
        if len(id) != 15:
            return id

        abc123 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ012345'
        abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        first_letter = 0 if id[0] not in abc else 1
        first_letter += 0 if id[1] not in abc else 2
        first_letter += 0 if id[2] not in abc else 4
        first_letter += 0 if id[3] not in abc else 8
        first_letter += 0 if id[4] not in abc else 16
        first_letter = abc123[first_letter]

        second_letter = 0 if id[5] not in abc else 1
        second_letter += 0 if id[6] not in abc else 2
        second_letter += 0 if id[7] not in abc else 4
        second_letter += 0 if id[8] not in abc else 8
        second_letter += 0 if id[9] not in abc else 16
        second_letter = abc123[second_letter]

        third_letter = 0 if id[10] not in abc else 1
        third_letter += 0 if id[11] not in abc else 2
        third_letter += 0 if id[12] not in abc else 4
        third_letter += 0 if id[13] not in abc else 8
        third_letter += 0 if id[14] not in abc else 16
        third_letter = abc123[third_letter]

        return id + first_letter + second_letter + third_letter

def fmt(format,value):
    if type(value) == str:  return ''
    try:
        if format == 'e':
            x = str(int(round(float(value/1.27),0)))
        else:
            x = str(int(round(float(value),0)))
    except:
        return '-'

    if format == 'd':
        if len(x) < 4:
            return '$'+x
        elif len(x) == 4:
            return '$'+x[0]+','+x[1:]
        elif len(x) == 5:
            return '$'+x[0:2]+','+x[2:]
        elif len(x) == 6:
            return '$'+x[0:3]+','+x[3:]
        elif len(x) == 7:
            return '$'+x[0]+','+x[1:4]+','+x[4:]
        elif len(x) == 8:
            return '$'+x[0:2]+','+x[2:5]+','+x[5:]
        elif len(x) == 9:
            return '$'+x[0:3]+','+x[3:6]+','+x[6:]

    elif format == 'e':
        if len(x) < 4:
            return '&euro;'+x
        elif len(x) == 4:
            return '&euro;'+x[0]+','+x[1:]
        elif len(x) == 5:
            return '&euro;'+x[0:2]+','+x[2:]
        elif len(x) == 6:
            return '&euro;'+x[0:3]+','+x[3:]
        elif len(x) == 7:
            return '&euro;'+x[0]+','+x[1:4]+','+x[4:]
        elif len(x) == 8:
            return '&euro;'+x[0:2]+','+x[2:5]+','+x[5:]
        elif len(x) == 9:
            return '&euro;'+x[0:3]+','+x[3:6]+','+x[6:]


    elif format == 'n':
        if len(x) < 4:
            return x
        elif len(x) == 4:
            return x[0]+','+x[1:]
        elif len(x) == 5:
            return x[0:2]+','+x[2:]
        elif len(x) == 6:
            return x[0:3]+','+x[3:]
        elif len(x) == 7:
            return x[0]+','+x[1:4]+','+x[4:]
        elif len(x) == 8:
            return x[0:2]+','+x[2:5]+','+x[5:]
        elif len(x) == 9:
            return x[0:3]+','+x[3:6]+','+x[6:]

    elif format == 'p':
        return str(x+'%')

    elif format == 'arrow':
            y = 0 - value
            if value > 0:
                return '&uarr; %i'%(value)
            elif value < 0:
                return '&darr; - %i'%(y)
            else:
                return '0'

def fix_tabs(file_name=False):
    if not file_name:
        file_name = str(eval(input('Enter a file to fix: ')))
    text = ''
    with open(file_name) as file:
        text = file.read()
        text.replace('\t','    ')
    with open(file_name,'w') as file:
        file.write(text)

def parse_domain(email):
    
    # 1. Get just the domain from the email passed in
    domain = email.split('@')[1].lower()
    top_level_domains = [
        'com',
        'org',
        'edu',
        'gov',
        'eu',
        'uk',
        'net',
        'ca',
        'de',
        'tv',
        'jp',
        'fr',
        'au',
        'us',
        'cn',
        'co',
        'io',
        'me',
        'ru',
        'ch',
        'it',
        'nl',
        'se',
        'no',
        'es',
        'mil',
        'the',
        'gw',
        'ax',
        'wf',
        'yt',
        'sj',
        'mobi',
        'eh',
        'mh',
        'bv',
        'ap',
        'cat',
        'kp',
        'iq',
        'um',
        'arpa',
        'pm',
        'gb',
        'cs',
        'td',
        'so'    
    ]
    # 2. Remove unwanted characters from domain
    clean_domain = domain.replace('-','').replace('_','')

    # 3. Split on the '.' and analyze the resulting list
    true_domain = []
    for d in clean_domain.split('.'):
        if d not in top_level_domains:
            true_domain.append(d)

    if len(true_domain) == 0:
        return clean_domain.split('.')[0]
    elif len(true_domain) == 1:
        return true_domain[0]
    else:
        return '.'.join(true_domain)



def get_gdoc(spreadsheet_name):
    import gspread
    from oauth2client.client import SignedJwtAssertionCredentials
    login = {
      "type": "service_account",
      "private_key_id": "3ceb72012a81f113cc5dd40fc5732dadba2d79b9",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCLz66N1KJcpbKF\nPE1fvmWpCvR2E9Is+dOTRqQLzenD78MSOaPQNNPNS9BgJOI+tfyRSRD/YyO55o7/\nVm58dW6LdgO3p1/aYPMUbfsN1UOjEf6DVwsVL9k5DMpHDDN4hIdgmEvkxWRguXkZ\nu2zMgqOd4VqBJLu/YAB8d+cB/Y+Gk+YoQb3V6kSkR/s0kmA5PVcD8B4DpKfQg+68\nbn0juDSjmHjhqVqVRJchlvbkbvi+0cj10GQQNPHWLTJrsqQPEuQqMXVGMcCEW3th\nBArIubJSxdlQuP0Z3DzLsq/eQmhDuW4jfxRF+8/LzQmJfn2rqK4ObkyOWP1kxiAx\ni6Zf+V9/AgMBAAECggEAPWCwTd2SZb/sbmd5xFWOxbZkec3b0BjhFF/HttLwFC+W\n4NJjIw1+CjuFQCARHtzAA3wjNSrtzTf1gQ0Nth/LpvfpS9/zyagULtzVgU4lwlos\n9LXqzKNT5qLBzo0Br5/m2rYhY05w8bGbA3vvmJylfbMoC1f4AF0B+aKdzJbnQnnW\nPiVDVO5Z1+aO7mf0XJLtX+wzeTgAst3nw8loBVTViYrah4tBNx0Tfn+BOM78sFKK\nVGJR4+dZ8HWniDx0q4vtWHcFeVCyD18QGzkFS8y1bOj4KOZxiaxwKDDfu/BvCBKv\njX4/ktBySMDMcOWyXGTC9D4qlTqQevr+whnNGFnjoQKBgQDTzglTFltefe/aMH/3\nFzvVcMLYtogYmTIi7tkhpTRvsg/iPRjrLI76AkjRMmlJWNsVjgstl1mhV8VsqEz/\nFZW5gxqCq6ODnwb9Za5Nzf+wKniEbTjC8ydkJSnSV+Uq9FG0N4e+csW1WYRc/LRd\niMKS871siz6gqVb6CE+0yh4UkQKBgQCo+/hJM5/jE+nJymWm8QVJxyBSINBXWQBb\nfP58uJnmQPGAmW0POpkintjXK0oEJcXGThgjZuqewIUeIPeIzdAfSWIU5uXMWvDS\ntF1SzY+ihtjbru+Y/gjaNgDV78jQku73zf/+BUCulb2277t+w56eElf6atwGyHKP\nLDExf0z7DwKBgBDlYsEKC4fiK/wP2mVvqQpB0IlRJlIwBlvbCd8xOpmebr3xecdo\n6o7vF7f4eYWsXO2/Qw0EAdZpFgqw8lN2+VavKrI51vVs/jXAosL6J+d5u9t0iw6i\nLwZCIK/y6wkeLFZgB6gdp7/rwC9ayViczEjEwNujz/8pAxM3DoSxiuzBAoGAa4Yw\n/TspII+aMjlkJy6zw7c93KRejUXnkU9eizPXUYi/Yqm9mHQb3sieh4NXDH6Qctdc\nSqKA5dTwnzQw7c6wAEhsbYpibH7tP9VekIKWQ790G40bjgkOzvKP45E5AWaNQgbF\nPfhPqQdE+TNf5ZBJzKE1c/Us3fAL3QgsoSc0b4cCgYEAsdAwcg97Jp4sxmHf4vl2\nnv6xNlK5zoz2S2doIPrKXem7jD+mTB//Ajjtvppw0wg4ZBdP3mQknBFkER7PUoqj\nMMPGgQEBIkoNTjHaNLjTcmZW589u6cU6PjNRKMlQ+wcrXGe3Wwu10ekE6qqf2ARr\ny9dKn/PdYlKPXLlVJuE4gb8=\n-----END PRIVATE KEY-----\n",
      "client_email": "clarus-designs@clarus-designs.iam.gserviceaccount.com",
      "client_id": "110476318102952152267",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/clarus-designs%40clarus-designs.iam.gserviceaccount.com"
    }
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(login['client_email'], login['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)
    
    return gc.open(spreadsheet_name)

def make_csv_from_dict(name,data):
    headers = []
    rows = []
    for d in data:
        if headers == []:
            headers = list(d.keys())
            rows.append(headers)
        row = []
        for f in headers:
            row.append(d[f])

        rows.append(row)
    write_csv(name,rows)

def make_date(format,date):
    date = str(date).split(' ')[0]
    if format == 'api':
        x = date.split('-')
        return str(str(x[1])+'-'+str(x[2])+'-'+str(x[0]))
    elif format == 'sortable':
        x = date.split('-')
        return str(str(x[2])+'-'+str(x[0])+'-'+str(x[1]))

def open_url(url,pause=False,instance='sumo'):
    import webbrowser
    if len(url) in [15,18] and '.' not in url:
        if instance=='sumo logic':
            print('open 1')
            webbrowser.open('https://na9.salesforce.com/'+url)
        if instance == 'intercom':
            webbrowser.open('https://na17.salesforce.com/'+url)
        else:
            print('open 2')
            webbrowser.open('https://na31.salesforce.com/'+url)
    else:
        if '://' not in url:
            print('open 3')
            webbrowser.open('http://'+url)
        else:
            print('open 4')
            webbrowser.open(url)
    if pause:
        eval(input('\nHit enter to continue\n'))


def send_email(recipients,subject,message,format='text',**kwargs):
    import smtplib
    from email.message import EmailMessage
    from email.headerregistry import Address
    from email.utils import make_msgid

    msg = EmailMessage()
    
    msg['Subject'] = subject
    msg['From'] = 'Ryan Cao'
    msg['To'] = ','.join(recipients) if type(recipients) != str else recipients
    gmail_user = 'cao2015ryan@gmail.com'
    gmail_pwd = 'Newpassword2*'
    if format == 'text':
        msg.set_content(message)
    else:
        msg_id = make_msgid()
        msg.add_alternative(message.format(msg_id=msg_id[1:-1]), subtype='html')
 
    attempts = 0
    while attempts < 5:
        attempts += 1
        try:
            # sends email
            smtpserver = smtplib.SMTP("smtp.gmail.com:587")
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            smtpserver.sendmail('Greg Dalli', recipients, msg.as_string())
            smtpserver.close()
            print(('Email Sent: %s' % recipients))
            break
        except Exception as e:
            print('ERROR: Pausing for 3 minutes')
            print(('\t %s' % e))
            from time import sleep
            sleep(180)

def send_sms(to_number, message):
    from twilio.rest import Client
    account_sid  = 'AC215e8e057dd7fc81835f5bfe1edc5803'
    auth_token  = '3c900415db7dd6153fe62a5f84a9eeb7'
    # Initiates session
    client = Client(account_sid, auth_token)

    # Sends message
    client.messages.create(
            to="+1%s" % str(to_number),
            from_="+14158020160",
            body= message
            )

def normalize_field_name(field):
    if '__c' in field:
        field = field.strip('__c')
        return field.lower()
    elif '.' in field:
        return field.replace('__c','').replace('.','_').lower()
    else:
        clean_field = ''
        for letter in field:
            if letter.lower() == letter:
                clean_field += letter
            else: 
                clean_field += '_'+letter.lower()
        return clean_field.strip('_')


def set_fields(obj,fields):

    for field in fields:
        
        value = fields[field]
        clean_field_name = field[0]
        field = field.replace('.','')
        for letter in field[1:]:
            if letter.upper() == letter and letter != '_':
                clean_field_name += '_'+letter
            else:
                clean_field_name += letter
        
        clean_field_name = clean_field_name.lower().replace('__c','').replace('__','_')
        setattr(obj,clean_field_name,value)         
    return obj

def stringify(text):
    from unicodedata import normalize
    if text == None:
        return ''
    elif type(text) == str:
        return normalize('NFKD', text).encode('ascii','ignore')
    else:
        return str(text)

def verify_email(email):
    from kickbox import Client
    client   = Client('83aa1f631deefcfec16c3c489fdfe831540bbbf1615b8cf8a2b8544c4fa9f09c')
    kickbox  = client.kickbox()
    
    # Here I log the different types of responses I can get back for system isues
    system_erros = ['invalid_email','no_connect','timeout','invalid_smtp','unavailable_smtp','low_quality','unexpected_error']
    key = 'b58eacc922aef6c2ef7a823cb092da4a77f6525474b0fb3101d339de772f89bf'

    results = (kickbox.verify(email,{'timeout':30000})).body
    
    if not 'success' in results:
        return ['Call Failed',results]
    elif not results['success'] and results['message'] != 'Insufficient balance':
        return ['Insifficient Balance! Stop Running',results]
    elif results['success']:
        verdict = results['reason']
        if results['accept_all']:
            return ['unknown-accepts-all',results]
        elif 'risky' in verdict or verdict in system_erros:
            return ['unknown-risky',results]
        elif verdict == 'accepted_email':
            return ['valid',results]
        elif verdict == 'rejected_email':
            return ['invalid',results]
        elif verdict == 'invalid_email':
            return ['invalid',results]
        elif verdict == 'invalid_domain':
            return ['invalid',results]
        else:
            return ['weird error',results]
    else:
        return ['Something really mssed up',results]
 
def typefy(input):
    import datetime
    try:
        return datetime.datetime.strptime(input, "%Y-%m-%d")
    except:
        try:
            x = input.replace('T',' ').replace('+00','')
            return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
        except:
            pass

    if type(input) == type('hello'):
        input = stringify(input)

    if input in ['true','True','False','false']:
        if input in ['true','True']:
            return True
        else:
            return False
    elif '.' in input:
        try:
            input = float(input)
            return input
        except:
            pass
    try:
        return int(input)
    except:
        return input

def write_csv(filename,list_of_rows):
    import csv
    import pandas as pd
    my_df = pd.DataFrame(rows)
    my_df.to_csv(filename, index=False, header=True)

def read_csv(name):
    import csv
    data = []
    with open(name) as file1:

        file = csv.reader(file1)
        for row in file:
            data.append(row)
    return data



class Salesforce():
    
    def __init__(self,instance='sumo'): 
        self.instance = instance
        self.connection = ''
        self.login()

    def login(self):
        from simple_salesforce import Salesforce        
        
        if self.instance =='kt':
            self.connection = Salesforce(username='greg@keeptruckin.com',password='Keeptruckin1!' ,security_token='Gumc1181XCq4oqNK5ndyiCoUm')

        if self.connection != '':
            print(('Logged in to SFDC %s instance' % self.instance))
        
        else:
            print('Failed to login')

    def merge(object,master,slave,sf,log_level=None,field_set =None,other_objects=[]):
        objects = [
            'Task',
            'Event',
        ].extend(other_objects)
        if object.lower() == 'account':
            objects.extend(['Opportunity','Contact',])
        
        # Move Records
        for o in objects:
            data = sf.query("SELECT Id FROM %s WHERE %sID = '%s'" % (o,obj,slave))
            if log_level.lower() in ['basic','detailed']:
                print(('\tMoving %i %s Records' % (len(data),o)))
            for record in data:
                method = getattr(self.connection,obj)
                method.update(record['Id'],{obj+'Id':master})
                if log_level.lower() == 'detailed':
                    print(('\t\tUpdated %s record' % o))
        # Copy data to master
        if field_set:
            if log_level:
                print('Copying blank fields to master')
            new = sf.query("SELECT  %s FROM %s WHERE Id = '%s'" % (','.join(field_set),obj,master))[0]              
            old = sf.query("SELECT  %s FROM %s WHERE Id = '%s'" % (','.join(field_set),obj,slave))[0]       
            new_data = {}
            for f in new:
                if new[f] == '' and old[f] != '':
                    new_data[f] = old[f]
            if len(new_data) > 0:
                method = getattr(self.connection,obj)
                method.update(master,new_data)
                
    def bulk(self,obj,action,data,interval=500):
        print(('Performing Bulk %s on %i %s records' % (action,len(data),obj)))
        obj = getattr(self.connection.bulk,obj)
        method = getattr(obj,action)
        good,bad,count = 0,0,0
        updates = []
        for d in data:
            count += 1
            updates.append(d)
            if len(updates) == interval or (len(updates) > 0 and count == len(data)):
                res = method(updates)
                for r in res:               
                    if r['success']:
                        good += 1
                    else: 
                        bad += 1
                        print((r['errors']))
                    print((good, '/',bad,'/',len(data)))
                    updates = []

    def update(self,object,record_id,new_info):
        obj = getattr(self.connection,object)
        return obj.update(record_id,new_info)      

    def query(self,query,update=False):
        
        from collections import OrderedDict

        all_records = []
        activity = self.connection.query(query)
        total_size = activity['totalSize']    
        if 'nextRecordsUrl' in activity:  
            next_query_url = activity['nextRecordsUrl']    
        all_records.extend(activity['records'])
        if update:
            print(('Querried %i of %i' % (len(all_records),total_size)))

        while len(all_records) < total_size:
            activity = self.connection.query_more(next_query_url,True)
            all_records.extend(activity['records'])
            if update:
                print(('Querried %i of %i' % (len(all_records),total_size)))
            if 'nextRecordsUrl' in activity:
                next_query_url = activity['nextRecordsUrl']    

        clean_records = []
        for record in all_records:
            
            num_dicts = 1
            clean_record = dict(record)
            while num_dicts != 0:
                num_dicts = 0
                temp_dict = {}
                for field in clean_record:

                    value = clean_record[field]
                    if type(value) == OrderedDict:
                        num_dicts += 1
                        value = dict(value)
                        for sub_field in value:
                            temp_dict['%s.%s' % (field,sub_field)] = value[sub_field]
                    elif 'attributes' not in field:
                        if value == None:
                            temp_dict[field] = ''
                        elif type(value) in [str,int,float,bool]:
                            temp_dict[field] = value
                        else:
                            temp_dict[field] = value.decode('utf-8')
                clean_record = temp_dict
            clean_records.append(temp_dict)
        return clean_records
            
    def count_contacts(self):
        accounts = {}
        data = self.query('select Id, AccountId from contact')
        
        for contact in data:    
            act = contact['AccountId']
            
            if act in accounts:
                accounts[act].append(contact['Id'])
            else:
                accounts[act] = []
                accounts[act].append(contact['Id'])
        return accounts          

    def delete(self,object,record_id):
        obj = getattr(self.connection,object)
        return obj.delete(record_id) 

class Database():
    # Used to interact with our database.  Example below:
    # db = Database()
    # db.log_field('sumo','ADB349DEW','Lead','lead_source__c','Sales')
    # entry = db.session.query(db.Fields).filter_by(company='sumo').all()

    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()    
        
    class Fields(Base):
        from datetime import datetime
        from sqlalchemy import Column, Integer, String, DateTime
        
        __tablename__ = 'fields'
        id = Column(Integer,primary_key=True)
        created_date = Column(DateTime, default=datetime.utcnow)
        company = Column(String(20))
        object_id = Column(String(18))
        object_type = Column(String(20))
        field_name = Column(String(30))
        field_value = Column(String)
   
        def __repr__(self):
            return "<Field(company='%s', field_name='%s', value='%s')>" % (self.company, self.field_name, self.field_value)
   
    class Emails(Base):
        from datetime import datetime
        from sqlalchemy import Column, Integer, String, DateTime
               
        __tablename__ = 'emails'
        id = Column(Integer,primary_key=True)
        email = Column(String(40),primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)
        status = Column(String(20))
        
        def __repr__(self):
            return "<Email(email='%s', status='%s')>" % (self.email, self.status)
   
    def __init__(self):
        
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker 
        
        self.engine = create_engine('postgres://nvnrmhxjbosymi:VBniA9F714gW3MqxIQf0PUTGGX@ec2-54-83-61-45.compute-1.amazonaws.com:5432/dbahmjn951vs8k')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    
    def commit(self):
        self.session.commit()


class Lead():
    
    def __init__(self):
        self.id = ''
        self.name = ''
        self.company = ''
        self.email = ''
        self.domain = ''
        self.owner_id = ''
        self.owner = ''
        self.object = 'Lead'

class Contact():

    def __init__(self):
        self.id = ''
        self.name = ''
        self.company = ''
        self.email = ''
        self.domain = ''
        self.account_id = ''
        self.account_name = ''
        self.account = ''
        self.owner_id = ''
        self.owner_name = ''
        self.owner = ''
        self.object = 'Contact'

class Account():

    def __init__(self):
        self.id = ''
        self.name = ''
        self.contacts = {}
        self.opportunities = {}
        self.owner_id = ''
        self.owner_name = ''
        self.owner = ''
        self.object = 'Account'

class Opportunity():

    def __init__(self):

        self.id = ''
        self.name = ''
        self.owner_id = ''
        self.owner_name = ''
        self.owner = ''
        self.object = 'Opportunity'
        self.opp_history = {}
        self.amount = 0
        self.stage = ''
        self.type = ''

class User():

    def __init__(self):

        self.id = ''
        self.name = ''
        self.is_active = True
        self.profile_id = ''
        self.profile_name = ''
        self.accounts = {}
        self.leads = {}
        self.opportunities = {}
        self.object = 'user'        

def print_exception():
    import linecache
    from sys import exc_info
    exc_type, exc_obj, tb = exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def best_fit_line(xs,ys):
    from statistics import mean
    import numpy as np

    xs = np.array(xs, dtype=np.float64)
    ys = np.array(ys, dtype=np.float64)
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    b = mean(ys) - m*mean(xs)
    return [m,b]

def predict(subject,m,b):
    predict_y = (m*subject)+b
    return predict_y

def squared_error(y_actual,y_predict):
    return sum((y_predict - y_actual) * (y_predict - y_actual))

def r_squared(y_actual,y_predict):
    y_mean_line = [mean(y_actual) for y in y_actual]
    squared_error_regr = squared_error(y_actual, y_predict)
    squared_error_y_mean = squared_error(y_actual, y_mean_line)
    return 1 - (squared_error_regr/squared_error_y_mean)

def train_k_nearest_neighbors(X,y):
    import numpy as np
    from sklearn import preprocessing, cross_validation, neighbors, svm
    import pandas as pd
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
    clf = neighbors.KNeighborsClassifier()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(accuracy)

def predict_k_nearest_neighbors(example_measures):
    prediction = clf.predict(example_measures)
    print(prediction)

def train_k_nearest_neighbors(X,y):
    import numpy as np
    from sklearn import preprocessing, cross_validation, neighbors, svm
    import pandas as pd
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
    clf = svm.SVC()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(accuracy)

import os

if os.path.isfile('clarus.pyc'):
    os.remove('clarus.pyc')

"""
CSM alert
CSE alert email
Create report fo unassigned accounts
follow up with josh about NPS fields not syncing
current macos type / 
"""
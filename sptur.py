import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socks
import io
import os
import stem.process
import re
import requests
from my_proxy_smtplib import ProxySMTP
import signal
import psutil
import argparse

parser = argparse.ArgumentParser(description ='Mail spammer')
parser.add_argument('-m', '--mail', dest = 'mailSender',
                    required = True,
                    help ='Insert the mail of the sender')
parser.add_argument('-p', '--Password', dest = 'passwordSender', 
                    required = True,
                    help ='Insert the password of the sender')
parser.add_argument('-l', '--mailList', dest = 'mailList', 
                    required = True, 
                    help ='Insert the file contaning the mailing list (file.txt)')
parser.add_argument('-s', '--subject', dest = 'subject', default ='',
                    help ='Insert the subject of the mail')
parser.add_argument('-t', '--text', dest = 'text', default ='',
                    help ='Insert the text of the mail')
parser.add_argument('-f', '--file', dest = 'file', default ='',
                    help ='Insert the file to attach at the mail')
parser.add_argument('-smtp', '--smtpServer', dest = 'smtp', default ='smtp.gmail.com', 
                    help ='Insert the smtp server to use')
parser.add_argument('-tp', '--tryProxy', dest = 'tentativiProxy', default ='20', 
                    help ='Insert the number of mail sent for proxy')
args = parser.parse_args()


mailSender = args.mailSender
passwordSender = args.passwordSender
mailList = args.mailList
subject = args.subject
text = args.text
file = args.file
smtp = args.smtp
tentativiProxy = args.tentativiProxy
print(
    






    )
    
try:
    print('Starting TOR proxy')
    SOCKS_PORT = 9050
    TOR_PATH = os.path.normpath(os.getcwd()+"\\Tor\\tor.exe")
    tor_process = stem.process.launch_tor_with_config(
    config = {
         'SocksPort': str(SOCKS_PORT),
          },
    init_msg_handler = lambda line: print(line) if re.search('Bootstrapped', line) else False,
    tor_cmd = TOR_PATH
    )
except OSError:
    for proc in psutil.process_iter():
        if proc.name() == 'tor.exe':
            proc.kill()
    tor_process = stem.process.launch_tor_with_config(
    config = {
         'SocksPort': str(SOCKS_PORT),
          },
    init_msg_handler = lambda line: print(line) if re.search('Bootstrapped', line) else False,
    tor_cmd = TOR_PATH
    )
    

print('TOR proxy started')


message = MIMEMultipart()
message["From"] = mailSender
message['Subject'] = subject
message['Body'] = subject
mailFile = open(mailList)
mailFileSending = open(mailList)
body = MIMEText(text)
message.attach(body)
if file!= '':
    attachment = open(file,'rb')
    obj = MIMEBase('application','octet-stream')
    obj.set_payload((attachment).read())
    encoders.encode_base64(obj)
    obj.add_header('Content-Disposition',"attachment; filename= "+file)
    message.attach(obj)
my_message = message.as_string()

email_session = ProxySMTP(smtp,587,
                          proxy_addr='127.0.0.1',
                          proxy_port=9050)
email_session.starttls()
email_session.login(mailSender, passwordSender)

n=0
for line in mailFile:
    reciver = mailFileSending.readline()
    email_session.sendmail(mailSender,reciver,my_message)
    n=n+1
    print('mail '+str(n)+' to '+ reciver)
    if n%tentativiProxy==0 :
        tor_process.kill()
        tor_process = stem.process.launch_tor_with_config(
          config = {
            'SocksPort': str(SOCKS_PORT),
              },
              init_msg_handler = lambda line: print(line) if re.search('Bootstrapped', line) else False,
          tor_cmd = TOR_PATH
            )
        
email_session.quit()
tor_process.kill()

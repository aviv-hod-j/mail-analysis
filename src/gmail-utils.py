import os
import yaml
import email
import imaplib
from bs4 import BeautifulSoup
import mimetypes
import re
import csv

# Login by credentials file
credentials_filename = 'credentials.yml'
credentials_path = os.path.join(os.getcwd(),credentials_filename)
with open(credentials_path, 'r') as mail_credentials:
    contents = yaml.load(mail_credentials)
    username = contents['username']
    password = contents['password']

    host = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(host) #encrypted method
    mail.login(username, password)
    mail.select('inbox')

# Collecting raw mails by ids in inbox
_, uids = mail.uid('search', None, 'ALL')
inbox_uids_lst = uids[0].split()

# list of dicts of metadate for postgres container (LATER_ON)
mails_meta_data = []

for mail_id in inbox_uids_lst:

    # fetching raw mails
    _, email_data = mail.uid('fetch', mail_id, '(RFC822)')
    raw_email = email_data[0][1].decode('utf-8')
    email_message = email.message_from_string(raw_email)

    # Collecting meta-data:
    metadata = {}
    for header in ['message-id', 'from', 'to', 'subject', 'date','content-type']:
        if header == 'from' or header == 'to':
            mail_address_match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', email_message[header])
            metadata[header] = mail_address_match
        else:
            metadata[header] = email_message[header]
    mails_meta_data.append(metadata)


    # Collecting mail contents:
    counter = 1
    for part in email_message.walk():
        if part.get_content_maintype == 'multipart':
            continue

        filename = part.get_filename()
        content_type = part.get_content_type()
        if not filename:
            ext = mimetypes.guess_extension(content_type)
            if not ext:
                ext = '.bin'
            elif 'html' in content_type:
                ext = '.html'
            elif 'text' in content_type:
                ext = '.txt'
            filename = 'msg-part-%08d%s' %(counter, ext)
        counter += 1

        
    # Saving attachments and contents
    save_path = os.path.join(os.getcwd(), 'raw', 'inbox','email_data', str(metadata['date'][5:16]).replace(" ","_"),str(metadata['from'])[2:-12])
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(os.path.join(save_path, filename), 'wb') as filepath:
        filepath.write(part.get_payload(decode=True))

        
# Saving meta-data
keys = [k for k in mails_meta_data[0].keys()]
file_name = str(mails_meta_data[0]['to'])[2:-2]+'_metadata.csv'


meta_save_path = os.path.join(os.getcwd(), 'raw', 'inbox', 'metadata')
if not os.path.exists(meta_save_path):
    os.makedirs(meta_save_path)

with open(os.path.join(meta_save_path, file_name), 'w',newline='') as outputfile:
    dict_writer = csv.DictWriter(outputfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(mails_meta_data)



 


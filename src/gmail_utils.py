import os
import yaml
import email
import imaplib
from bs4 import BeautifulSoup
import mimetypes
import csv
from mail_metadata import MailMetadata


class MailController:

    host = 'imap.gmail.com'

    def __init__(self, credentials_path=None):
        self.credentials_path = credentials_path
        self.mail = None

    def _get_credentials(self):
        with open(self.credentials_path, 'r') as mail_credentials:
            contents = yaml.safe_load(mail_credentials)
        return {'username': contents['username'], 'password': contents['password']}

    def login_by_credentials(self):
        credentials = self._get_credentials()
        self.mail = imaplib.IMAP4_SSL(self.host) #encrypted method
        self.mail.login(credentials['username'], credentials['password'])
            
    def get_inbox(self):
        self.mail.select('inbox')


    def get_uids_list(self):
        _, uids = self.mail.uid('search', None, 'ALL')
        uids_lst = uids[0].split()
        return uids_lst

# list of dicts of metadate for postgres container (LATER_ON)
# mails_meta_data = []
# for mail_id in uids_lst:

    def get_raw_mail_by_id(self, uid):
        _, email_data = self.mail.uid('fetch', uid, '(RFC822)')
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        return email_message


    def __str__(self):
        return f"credential = {self.credentials_path}, mail = {self.mail}"



    # def get_contents_by_id(self, uid):
    #     counter = 1
    #     for part in email_message.walk():
    #         # if part.get_content_maintype == 'multipart':
    #         #     continue

    #         filename = part.get_filename()
    #         content_type = part.get_content_type()
    #         if not filename:
    #             ext = mimetypes.guess_extension(content_type)
    #             if not ext:
    #                 ext = '.bin'
    #             elif 'html' in content_type:
    #                 ext = '.html'
    #             elif 'text' in content_type:
    #                 ext = '.txt'
    #             filename = 'msg-part-%08d%s' %(counter, ext)
    #         counter += 1

        
#     # Saving attachments and contents
#     save_path = os.path.join(os.getcwd(), 'raw', 'inbox','email_data', str(metadata['date'][5:16]).replace(" ","_"),str(metadata['from'])[2:-12])
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     with open(os.path.join(save_path, filename), 'wb') as filepath:
#         filepath.write(part.get_payload(decode=True))

        
# # Saving meta-data
# keys = [k for k in mails_meta_data[0].keys()]
# file_name = str(mails_meta_data[0]['to'])[2:-2]+'_metadata.csv'


# meta_save_path = os.path.join(os.getcwd(), 'raw', 'inbox', 'metadata')
# if not os.path.exists(meta_save_path):
#     os.makedirs(meta_save_path)

# with open(os.path.join(meta_save_path, file_name), 'w',newline='') as outputfile:
#     dict_writer = csv.DictWriter(outputfile, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(mails_meta_data)



 


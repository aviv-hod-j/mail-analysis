from dataclasses import dataclass
from datetime import datetime
from typing import List
import re
from email.header import decode_header

@dataclass
class MailMetadata:

    message_id: str
    sent_by: List[str]
    sent_to: List[str]
    subject: str
    mail_time: datetime
    content_type: str

    @staticmethod
    def key_mapper():
        headers = {'message-Id': 'message_id',
                   'from': 'sent_by',
                   'to': 'sent_to',
                   'subject': 'subject',
                   'date': 'mail_time',
                   'content-type': 'content_type'}
        return headers

def metadata_obj_from_raw_mail(raw_mail):
    metadata = dict()
    header_mapper = MailMetadata.key_mapper()
    for header in header_mapper.keys():
        if header == 'from' or header == 'to':
            mail_address_match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', raw_mail[header])
            metadata[header_mapper[header]] = mail_address_match
        else:
            decoded_header = decode_header(raw_mail[header])[0][0]
            if isinstance(decoded_header, str):
                 metadata[header_mapper[header]] = decoded_header
            else:
                metadata[header_mapper[header]] = decoded_header.decode('utf-8')
    return metadata


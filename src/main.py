from gmail_utils import MailController
from mail_metadata import metadata_obj_from_raw_mail
import base64

if __name__ == '__main__':
    credential_path = r"C:\Users\Aviv's PC\Desktop\yh_law\gmail-utils\credentials.yml"
    conn = MailController(credential_path)
    conn.login_by_credentials()
    conn.get_inbox()
    ids_lst = conn.get_uids_list()

    """getting metadata:"""
    for uid in ids_lst:
        raw_mail = conn.get_raw_mail_by_id(uid)
        meta_data = metadata_obj_from_raw_mail(raw_mail)
        print(meta_data)
        break
        
        
    # print(conn)
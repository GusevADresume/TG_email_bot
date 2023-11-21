import imaplib
import email
from email.header import decode_header
import base64
import re
from config import mail_pass, mail_address, imap_server, incoming_address
import quopri


def checkMail():
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(mail_address, mail_pass)
    imap.select("INBOX")
    mail_num = imap.search(None, "UNSEEN")[1][0]
    if len(mail_num) > 0:
        msg = imap.fetch(mail_num, '(RFC822)')
        msg_obj = email.message_from_bytes(msg[1][0][1])
        payload = msg_obj.get_payload()
        if msg_obj['Resent-From'] == incoming_address or incoming_address in msg_obj['From']:
            data_to_tg = []
            for part in msg_obj.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    data_to_tg.append(clean_body(get_body(part)))
                if part.get_content_maintype() == 'application':
                    data_to_tg.append(get_attachments(part))
            return data_to_tg


def get_body(part):
    if part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] in ("binary", "8bit", "7bit", None):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:
        return part.get_payload()


def from_subj_decode(msg_from_subj):
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1]
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return None


def get_attachments(part):
    attachments = list()
    if part.get_content_disposition() == "attachment":
        attachments.append(part.get_payload(decode=True))
        attachments.append(from_subj_decode(part.get_filename()))
    return attachments


def encode_att_names(str_pl):
    enode_name = re.findall("\=\?.*?\?\=", str_pl)
    if len(enode_name) == 1:
        encoding = decode_header(enode_name[0])[0][1]
        decode_name = decode_header(enode_name[0])[0][0]
        decode_name = decode_name.decode(encoding)
        str_pl = str_pl.replace(enode_name[0], decode_name)
    if len(enode_name) > 1:
        nm = ""
        for part in enode_name:
            encoding = decode_header(part)[0][1]
            decode_name = decode_header(part)[0][0]
            decode_name = decode_name.decode(encoding)
            nm += decode_name
        str_pl = str_pl.replace(enode_name[0], nm)
        for c, i in enumerate(enode_name):
            if c > 0:
                str_pl = str_pl.replace(enode_name[c], "").replace('"', "").rstrip()
    return str_pl


def clean_body(text=str):
    reg = re.compile('[^а-яА-я a-zA-Z 0-9 / . \n]')
    return (reg.sub('', text))

# -*- coding: utf-8 -*-
import smtplib

from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

from tornado import gen
import json


class HtmlSmtpMail(object):
    def __init__(self, smtp_server, smtp_user, smtp_password,
                 from_addr, to_addr, subject):
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject

    def read_file(self, file):
        with open(file, 'r')  as f:
            return f.read()

    def format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr(
            (
                Header(name, 'utf-8').encode(),
                addr.encode('utf-8') if isinstance(addr, unicode) else addr
            )
        )

    def mail_content(self, content, content_type):
        msg = ''
        if 'json' == content_type:
            content = json.dumps(content, ensure_ascii=False, indent=2)
            msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        elif 'html' == content_type:
            msg = MIMEText(content, _subtype='html', _charset='utf-8')

        msg['From'] = self.format_addr(self.from_addr)
        for index, addr in enumerate(self.to_addr):
            self.to_addr[index] = self.format_addr(addr)
        msg['To'] = ','.join(self.to_addr)
        msg['Subject'] = Header(self.subject, 'utf-8').encode()
        return msg.as_string()

    @gen.coroutine
    def send_mail(self, content, content_type):
        content = self.mail_content(content, content_type)
        smtp = smtplib.SMTP(self.smtp_server)
        try:
            smtp.login(self.smtp_user, self.smtp_password)
            smtp.sendmail(self.from_addr, self.to_addr, content)
        finally:
            smtp.quit()


import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailSender:
    if __name__ == '__main__':
        def __init__(self, login, password):
            self.login = login
            self.password = password
            self.subject = ''
            self.recipients = ''
            self.message = ''
            self.header = ''
            self.msg = ''
            self.ms = ''
            self.gmail_smtp = "smtp.gmail.com"
            self.gmail_imap = "imap.gmail.com"
            self.mail = ''
            self.criterion = ''
            self.latest_email_uid = ''
            self.result = ''
            self.data = ''
            self.raw_email = ''
            self.email_message = ''

        def send_message(self, subject, recipients, message, header=None):
            self.subject = subject
            self.recipients = recipients
            self.message = message
            self.header = header

            self.msg = MIMEMultipart()
            self.msg['From'] = self.login
            self.msg['To'] = ', '.join(self.recipients)
            self.msg['Subject'] = self.subject
            self.msg.attach(MIMEText(self.message))

            self.ms = smtplib.SMTP(self.gmail_smtp, 587)
            # identify ourselves to smtp gmail client
            self.ms.ehlo()
            # secure our email with tls encryption
            self.ms.starttls()
            # re-identify ourselves as an encrypted connection
            self.ms.ehlo()

            self.ms.login(self.login, self.password)

            ######

            self.ms.sendmail(self.login)
            self.ms.quit()
            print('Mail send.')

        def recieve_messages(self): #как это получение вообще чет без понятия как работает
            self.mail = imaplib.IMAP4_SSL(self.gmail_imap)
            self.mail.login(self.login, self.password)
            self.mail.list()
            self.mail.select("inbox")
            self.criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
            self.result, self.data = self.mail.uid('search', None, self.criterion)
            assert self.data[0], 'There are no letters with current header'
            self.latest_email_uid = self.data[0].split()[-1]
            self.result, self.data = self.mail.uid('fetch', self.latest_email_uid, '(RFC822)')
            self.raw_email = self.data[0][1]
            self.email_message = email.message_from_bytes(self.raw_email)
            self.mail.logout()

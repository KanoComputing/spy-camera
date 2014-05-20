# Copyright (c) Senthil Seveelavanan 2014
#
# This software may be used and distributed
# according to the terms of the GNU General Public License version 2, incorporated
# herein by reference.


from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


class EmailServer:
    def __init__(self, username, password, smpt_server_url, user_email=None):
        self.username, self.password = username, password
        self.smpt_server_url = smpt_server_url
        # for gmail username == user_email, but might be different for other
        # email providers
        self.user_email = user_email if user_email else username

    def create_email(self, subject, text, alternative_text):
        # Create the root message and fill in the email, to_email, and subject headers
        self.msgRoot = MIMEMultipart('related')
        self.msgRoot['Subject'] = subject
        self.msgRoot['email'] = self.user_email
        #self.msgRoot['beto_email'] = email
        self.msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to_email display.
        msgAlternative = MIMEMultipart('alternative')
        self.msgRoot.attach(msgAlternative)

        msgText = MIMEText(alternative_text)
        msgAlternative.attach(msgText)

        # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText(text, 'html')
        msgAlternative.attach(msgText)

        # reset id (counter)
        self.id = 0

    def send_email(self, email):
        self.msgRoot['beto_email'] = email
        # Send the email (this example assumes SMTP authentication is required)
        import smtplib
        smtp = smtplib.SMTP(self.smpt_server_url, 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.username, self.password)
        smtp.sendmail(self.user_email, email, self.msgRoot.as_string())
        smtp.quit()

    def attach_file_image(self, image_file):
        # This example assumes the image is in the current directo_emailry
        fp = open(image_file, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image{0}>'.format(self.id))
        self.msgRoot.attach(msgImage)
        # id counter
        self.id += 1

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 5:
        # first argument is the filename, so ignore
        send_email, username, password, smpt_server_url = sys.argv[1:]
        es = EmailServer(username, password, smpt_server_url)
    elif len(sys.argv) == 6:
        send_email, username, password, smpt_server_url, email = sys.argv[1:]
        es = EmailServer(username, password, smpt_server_url, email)
    else:
        raise ValueError('wrong number of arguments')

    subject = 'this is my subject'
    text = '<b>Captured!<br><img src="cid:image0"><br><br><img src="cid:image1">'
    alternative_text = 'my alternative_text'
    es.create_email(subject, text, alternative_text)
    es.attach_file_image('test.jpg')
    es.attach_file_image('test.jpg')
    es.send_email(send_email)


# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# Create the container (outer) email message.
from email.mime.text import MIMEText


def NotifyUsers(message):
    msg = MIMEMultipart()
    msg['Subject'] = 'Arbitrage Notification..!!'
    me = "mahmoudebeed1988@gmail.com"
    family = ["mah.ebid.cs@gmail.com"]
    msg['From'] = me
    msg['To'] = ', '.join(family)
    # Send the email via our own SMTP server.
    server = smtplib.SMTP('smtp.gmail.com:587')
    msg.attach(MIMEText(message, 'plain'))
    #msg.attach(MIMEText(message))
    username = 'mahmoudebeed1988@gmail.com'
    password = 'VisualC++Java!@#'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    text = msg.as_string()
    server.sendmail(me, family, text)
    server.quit()

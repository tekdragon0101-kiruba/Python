"""
To Use gmail, you need to enable 'app password' for sending mail from sender gmail id.
If not enable, it will not working, reports: 'authentication not accepted.' from gmail. 
"""
# Author: kirubakaran K
# Project title: ScrapIt-MailIt

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import re

# getting the current time of sending the news mail
now = datetime.datetime.now()

# scraping the heading content in hackernews website
# news.ycombinator.com


def extract_news(url):
    print('Extracting Hacker News Stories:')
    contents = ''
    contents += ('<h2><b>HackerNews Top Stories:</b></h2>\n' +
                 '<br>'+'-'*50+'<br>')
    n = 1
    # getting the html doc of website
    page = requests.get(url)
    # storing source of html in source variable
    source = page.content
    soup = BeautifulSoup(source, 'lxml')
    for span_tag in soup.find_all('span', {'class': 'titleline'}):
        a_tag = span_tag.find('a')
        contents += str(n) + ' :: ' + a_tag.text + '(' + \
            grep_link_from_a_tag(a_tag.get('href'))+')' + "\n" + "<br>"
        n += 1
    print('Mail composing...')
    return contents


def grep_link_from_a_tag(word):
    m = re.search(r'(https?:\/\/)\w+\.?([\w+]+\.[a-z]{2,})', word)
    if m:
        link = m.group(2)
    else:
        link = 'click here'
    return '<a href="'+word+'">'+link+'</a>'


def components_for_sending_mail(sender, receiver):
    SERVER = 'smtp.gmail.com'
    PORT = 587  # for starttls
    FROM = sender  # from email id
    TO = receiver  # to email id
    # athentication of from's email id
    PASSWD = '' # put you password here
    #input('Enter the password: ')
    print('OK')
    # creating the body of a mail
    msg = MIMEMultipart()
    msg['Subject'] = 'Top News Stories of HackerNews [Automated Email]' + \
        str(now)
    # + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(content, 'html'))
    sending_email_thro_smpt_server(SERVER, PORT, FROM, TO, PASSWD, msg)


def sending_email_thro_smpt_server(server_addr, port, f, t, pass_, msg):
    print('Server Initializing...')
    server = smtplib.SMTP(server_addr, port)
    # server.debuglevel()
    server.ehlo()
    server.starttls()
    # login thro credentials
    server.login(f, pass_)
    server.sendmail(f, t, msg.as_string())
    print('Email Sent.')
    server.quit()


content = extract_news('https://news.ycombinator.com/')
content += ('<br>'+'-'*50+'<br>'+'<br>End of the message<br>')
components_for_sending_mail(
    'set sender email', 'set receiver email')

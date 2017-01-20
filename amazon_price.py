from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
import ConfigParser

def logOutput(output):
	print '[AMAZON PRICE ALERT]: {0}'.format(output)

config = ConfigParser.ConfigParser()
config.read('config.ini')

TARGET_PRICE = int(config.get('AmazonSettings', 'TARGET_PRICE'))
AMAZON_LINK = config.get('AmazonSettings', 'AMAZON_LINK')
AMAZON_PRODUCT = config.get('AmazonSettings', 'AMAZON_PRODUCT')

RECEPIENT_EMAIL = config.get('EmailSettings', 'RECEPIENT_EMAIL')
SENDER_EMAIL = config.get('EmailSettings', 'SENDER_EMAIL')
SENDER_PASSWORD = config.get('EmailSettings', 'SENDER_PASSWORD')
SMTP_SERVER = config.get('EmailSettings', 'SMTP_SERVER')
SMTP_PORT = int(config.get('EmailSettings', 'SMTP_PORT'))

request_page = requests.get(AMAZON_LINK)

soup = BeautifulSoup(request_page.text, 'html.parser')

amazon_price_obj = soup.find('span', 'a-size-base a-color-price offer-price a-text-normal', recursive=True)

try:
	#if the price was unable to be found, amazon_price_obj is type 'NoneType', and the below command will throw an exception
	AMAZON_PRICE = float(amazon_price_obj.string.split('$')[1])
except:
	logOutput('Price unavailable')
	AMAZON_PRICE = TARGET_PRICE + 1

if (AMAZON_PRICE < TARGET_PRICE):
	logOutput('Price dropped! Sending email...')
	msg = MIMEText('The price for the {0} has dropped to ${1}.\r\n\r\nYou can view the product listing here: {2}'.format(AMAZON_PRODUCT, str(AMAZON_PRICE), AMAZON_LINK))
	msg['Subject'] = 'Automated Price Alert'
	msg['From'] = SENDER_EMAIL
	msg['To'] = RECEPIENT_EMAIL
	smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
	smtp.sendmail(SENDER_EMAIL, RECEPIENT_EMAIL, msg.as_string())
	smtp.quit()
	logOutput('Email sent!')
else:
	logOutput('Price didn\'t drop yet')

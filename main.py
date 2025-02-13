import requests
from bs4 import BeautifulSoup
from webserver import keep_alive
import schedule
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

url = 'https://jellycat.com/sky-dragon/'

header = {
  'User-Agent':
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'
}



# Set up the email parameters
sender = 'gleb.orlov8@gmail.com'
password = 'yyxopgoplfvmddbr'
recipient = 'gleb.orlov8@gmail.com'
subject = 'DRAGON IN STOCK'
body = '\U0001F525\U0001F525\U0001F525 ' + url

# Create the message object
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

in_stock = False

def send_email():
  # Create the SMTP session
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(sender, password)

  # Send the email
  text = msg.as_string()
  server.sendmail(sender, recipient, text)
  server.quit()


def start_monitor():
  response = requests.get(url, headers=header)
  soup = BeautifulSoup(response.text, 'html.parser')

  label = soup.find(
    'input', {
      'id': 'form-action-addToCart',
      'disabled': False,
    })
  global in_stock


  if label is  None:
    in_stock = False
    print('Out of Stock!')
  else:
    in_stock = True
    print('In Stock!')
    send_email()


def main():
  rnd = int(random.uniform(1, 5))
  print('rnd: ' + str(rnd))
  schedule.every(rnd).seconds.do(start_monitor)

  while not in_stock:
    schedule.run_pending()
    time.sleep(1)


keep_alive()
main()

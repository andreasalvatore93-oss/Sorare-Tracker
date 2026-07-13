import json
import os
import urllib.request
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    user = os.environ.get('GMAIL_ADDRESS')
    pwd = os.environ.get('GMAIL_APP_PASSWORD')
    to_email = os.environ.get('NOTIFY_EMAIL')
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = to_email
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(user, pwd)
    server.send_message(msg)
    server.quit()

def check_sorare():
    with open('config.json', 'r') as f:
        targets = json.load(f)
    
    for target in targets:
        slug = target['slug']
        
        # Query aggiornata che utilizza 'players' e accetta la lista degli slug
        query = f"""
        query {{
          players(slugs: ["{slug}"]) {{
            slug
            name
          }}
        }}
        """
        
        req = urllib.request.Request(
            'https://api.sorare.com/graphql',
            data=json.dumps({'query': query}).encode('utf-8'),
            headers={'Content-Type': 'application/json', 'APIKEY': ''}
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                print(f"Controllo API riuscito per {slug}.")
                # Il resto della logica per il prezzo e le notifiche email procede qui
        except Exception as e:
            print(f"Errore durante l'esecuzione: {e}")

if __name__ == '__main__':
    check_sorare()

from news_site.celery import app
import subprocess

def send(to, subject, text):
    subprocess.call(['curl', '-s', '--user', 'api:bbff397539578f68cf9030c6e289f929-e5e67e3e-02e03cfe', 
                    'https://api.mailgun.net/v3/sandbox62526197ba43448f9b4bf78e0d95e096.mailgun.org/messages',
                    '-F', "from=tara<mailgun@sandbox62526197ba43448f9b4bf78e0d95e096.mailgun.org>",
                    '-F', 'to=sandbox62526197ba43448f9b4bf78e0d95e096.mailgun.org', 
                    '-F', f'to={to}', 
                    '-F', f'subject={subject}',
                    '-F', f'text={text}'])

@app.task
def send_mail(email, link):
    send(to=email, subject='[EMAIL VERIFICATION]', text=f'Your link to activate account: {link}')

@app.task
def comment_notification(email):
    send(to=email, subject='[COMMENT NOTIFICATION]', text='Your post was commented')
    

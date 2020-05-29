from django.core.mail import EmailMultiAlternatives

def send(user_email):
    '''send email via mailgun'''
    subject = "Registration on news site"
    text_content = "Your veryfication link: ....."
    sender = "registration@mail"
    receipient = f"{user_email}"
    msg = EmailMultiAlternatives(subject, text_content, sender, [receipient])
    response = msg.send()
    print(response)
    return response
    # do something with response

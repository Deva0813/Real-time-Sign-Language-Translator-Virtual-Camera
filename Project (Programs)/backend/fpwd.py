from email.message import EmailMessage
import smtplib
import backend.mongo as mongo
import random

sender = "[TEST EMAIL]"
pwd = "[TEST PASSWORD]"
receiver = ""
otp=""
user_otp =""

def sendmail(email):
    global receiver
    receiver = email
    details = mongo.show(email)
    print(email)
    
    subject = "Password Reset Request"
    msg = "Hello "+details["name"]+", \n\nWe received a request of forget password for your account. \n\nThis is your password ' "+details["password"]+" ' of the requested Account registered to "+details["email"]+" .\n\nPlease note that this is a confidential matter and we advise you to keep your password safe. \n\nThank You,\nTeam RTSLT"
         
    message = EmailMessage()
    message['From'] = "RTSLT Server <TEST EMAIL>"
    message['To'] = receiver
    message['Subject'] = subject
    message.set_content(msg)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()   
        server.starttls()
        server.login(sender, pwd)
        server.sendmail(sender, receiver, message.as_string())
        print("Email sent successfully")
        
    except Exception as e:
        print("Error: unable to send email")
        print(e)

    finally:
        server.quit()
        
def otp(email):
    global receiver,otp
    receiver = email
    print(email)
    otp = random.randint(000000,999999)
    
    subject = "OTP for Account Creation"
    msg="Hello, \n\nThis is your OTP for account creation "+str(otp)+" of the created Account registered to "+email+" .\n\nPlease note that this is a confidential matter and we advise you to keep your password safe. \n\nThank You,\nTeam RTSLT"
    
    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.set_content(msg)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender, pwd)
        server.sendmail(sender, receiver, message.as_string())
        print("Email sent successfully")
        
    except Exception as e:
        print("Error: unable to send email")
        print(e)

    finally:
        server.quit()
    
    print("OTP sent successfully")
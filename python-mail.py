

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


msg = MIMEMultipart('alternative')

def credentials():
    try:
        with open('credentials.txt', 'r') as f:
           data=f.readlines()
           username=data[0]
           password=data[1]
    except FileNotFoundError as err:
        print(err)
    return username,password


def sendMail(sender, sender_password,from_name, recive, msg_str):
    HOST = 'smtp.gmail.com'
    PORT = 587
    server=smtplib.SMTP(HOST,PORT)
    server.ehlo()
    server.starttls()
    server.login(sender,sender_password)
    server.sendmail(from_name,recive,msg_str)
    server.quit()
    print("\nMail sent successfully!!")

def mailBody():
    try:
        f = open('text.txt', 'w')
    except FileNotFoundError as err:
            print(err)
    print("\n")
    print("Enter the text, when you are done type END")
    while True:
        text = input("New line of body: ")
        f.write(text)
        f.write("\n")
        if text=="END":  
            f.close()
            break
    try:
        with open('text.txt','r') as f:
            data=f.readlines()[:-1]
            data_string=''.join(data)
    except FileNotFoundError as err:
        print(err)
    return data_string 


def mailStructure (): 

    choice = input("Do you want to send this mail as plan ('p') or html ('h') ?: ")

    text = mailBody()

    if choice == 'h':
        html_part = MIMEText("<h1>" + text + "</h1>",'html')
        msg.attach(html_part)

    if choice == 'p':
        txt_part = MIMEText(text, 'plain')
        msg.attach(txt_part)
    
    msg_str=msg.as_string()
    return msg_str

def main():
    sender, sender_password=credentials()


    from_name=input("The FROM NAME: ")
    email_subject=input("Email subject: ")

    msg['From'] = from_name
    msg['Subject'] = email_subject


    print("1. Send mail to one adress")
    print("2. Send mail to multiple adresses")

    choice=int(input())

    if choice == 1:

        recive=input("Send email to: ")
        
        msg['To'] = recive

        msg_str = mailStructure()
        
        sendMail(sender,sender_password,from_name,recive,msg_str)
    

    if choice == 2:
        host = 'smtp.gmail.com'
        port = 587
        server=smtplib.SMTP(host,port)
        server.ehlo()
        server.starttls()
        server.login(sender,sender_password)

        msg_str = mailStructure()

        mails = []

        while True:

            receivers=input("Send email to: ")
            mails.append(receivers)

            if receivers == 'END':
                break
        for mail in mails[:-1]:
            msg['To'] =", ".join(mail)
            server.sendmail(from_name,mail,msg_str)
            server.quit()

if __name__=='__main__':
    main()

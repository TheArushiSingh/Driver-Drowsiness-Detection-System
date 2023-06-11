import smtplib
from email.message import EmailMessage
import imghdr
from current_location import current_location
def mail_owner(receiver_name,receiver_mail,driver_name,imagename):
    loc_link = current_location()
    SENDER_MAIL = "hj5658@srmist.edu.in" #ENTER YOUR SAMPLE EMAIL
    PASSWORD = "erp@SR21" #FILL YOUR OWN PASSWORD HERE
    msg = EmailMessage()
    msg['Subject'] = f'{driver_name.upper()} IS FEELING DROWSY!'
    msg['From'] = SENDER_MAIL
    msg['To'] = receiver_mail
    linkContent = f'<h3><a href="{loc_link}">Click this link to see his current location</a></h3>'
    html_content="""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                #warn{
                    background-color: #ffcc00;
                    font-color: #ffffff;
                    font-size: 44px;
                    vertical-align: middle;
                    padding: 2px;
                    margin: 0;
                }
                span{
                    padding-bottom: 40px;
                }
                #backdrop{
                    background-color: white;
                    font-color: black;
                    margin: 0;
                    padding: 10px;
                }
            </style>
        </head>
        <body>
            <div id="warn"><img src="https://cdn.clipart.email/ea68298e8daa254ad59564b3545b079a_warning-sign-warning-icons-transparent-background-png-clipart-_800-800.jpeg" height="65" width="65"></img>&nbsp;&nbsp;<span> ALERT!</span></div>
            <div id="backdrop">
                <h2 style>Hello """+receiver_name+""",</h2>
                <h4>This is to inform you that """+driver_name+""" is feeling drowsy so you can alert him and check his well being.</h4>"""+linkContent+"""
            </div>
        </body>
        </html>
        """
    msg.add_attachment(html_content,subtype="html")

    with open(imagename,'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(file_data,maintype="image",subtype=file_type,filename=file_name)

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(SENDER_MAIL, PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    mail_owner("Harsh","mansi","harshking6@gmail.com","wb.png")

import smtplib
import imaplib

keywords = ['restart', 'masterlock-stop','ping','force-poll']

#log in to servers and get ready to do stuff


#def startUp():
    
    #set the list of keywords, and do something if one is found
    
##def connect():
##    mail.connect()

#this will text a number with the desired text
def textUser(text):
    mail = smtplib.SMTP_SSL('smtp.gmail.com')
    mail.ehlo()
    mail.login('purplebotmail@gmail.com','purplemango1234')
    mail.sendmail('purplebotmail@gmail.com','5157243855@vtext.com',text)
    mail.close()

#this will look through the current emails in the folder, and
#look for keywords, if there are any requested, it will return
#a list of those keywords
def processEmails():
    global keywords
    msrvr = imaplib.IMAP4_SSL('imap.gmail.com',993)
    msrvr.login('purplebotmail@gmail.com','purplemango1234')
    
    keywordsFound = []
    msrvr.select('Inbox')
    typ, data = msrvr.search(None, 'ALL')
    for num in data[0].split():
        typ, data = msrvr.fetch(num, '(UID BODY[TEXT])')
        for key in keywords:
            if key in str(data[0][1])[2:-5].lower().split():
                keywordsFound.append(key)
        msrvr.store(num, '+FLAGS', '\\Deleted')
    msrvr.expunge()
    msrvr.close()
    msrvr.logout()
    return(keywordsFound)

###this function will ensure that you are logged in to the email server
##def logStart():
##    startUp()
##    processEmails()
##    
###this closes everything up
##def closeOut():
## msrvr.close()
## msrvr.logout()
 

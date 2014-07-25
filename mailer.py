import imaplib
import smtplib
from random import shuffle
import os
import re
import sys
import email
from email.parser import HeaderParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage

class Mailer(object):

  def __init__(self,subject):
    self.account = 'reevemoke@gmail.com'
    self.passwd = 'stemirepxe381scee'
    self.tag = subject
    self.mids = []
    self.current = None
    self.conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    self.conn.login(self.account, self.passwd)
    self.conn.select()

  def __str__(self):
    print "Mailer object for "+self.account

  def hasCurrent(self):
    return self.current!=None

  def getMessages(self):
    self.conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    self.conn.login(self.account, self.passwd)
    self.conn.select()
    msgIds = [int(x) for x in self.conn.search(None, 'UnSeen')[1][0].split()]
 
    for id in msgIds:
      data = self.conn.fetch(id, '(BODY[HEADER])')
      header_data = data[1][0][1]

      parser = HeaderParser()
      msg = parser.parsestr(header_data)
      if self.tag in msg['Subject'] and \
        self.account[:self.account.find("@")] not in msg["From"]:
        self.mids.append(id)
      
  def reply(self,name,corr,tim,mem):
    if self.current==None:
      print "No current message"
    new = MIMEMultipart("mixed")
    body = MIMEMultipart("alternative")
    replytxt = self.replyTxt(name,corr,tim,mem)
    body.attach(MIMEText(replytxt,"plain"))
    body.attach(MIMEText("<html>"+replytxt+"</html>","html"))
    new.attach(body)

    new["Message-ID"] = email.utils.make_msgid()
    new["In-Reply-To"] = self.current["Message-ID"]
    new["Subject"] = "Re: "+self.current["Subject"]
    new["To"] = self.current["Reply-To"] or self.current["From"]
    new["From"] = self.account
    try:
      s = smtplib.SMTP('smtp.gmail.com',587)
      s.ehlo()
      s.starttls()
      s.ehlo()
      s.login(self.account,self.passwd)
      s.sendmail(self.account,[new["To"]], new.as_string())
      s.quit()
    except Exception as e:
      print "Could not send reply to "+name

  def replyTxt(self,name,correct,time,memory):
    if os.path.isfile("./results.txt"):
      F = open("./answer.txt","r")
      expected = F.read()
      F.close()
      F = open("./results.txt","r")
      received = F.read()
      F.close()
    s = "<p>Dear "+name+",</p>"
    s += "<p>Thank you for submitting. Here are your statistics:</p>"
    if (correct==1):
      s += "<p>Your program's output was correct</p>"
      s += "<p><u> Expected Output:</u></p>"
      s += expected
      s += "<p><u> Student Output:</u></p>"
      s += received
    elif (correct==-1):
      s += "<p>Your program did not compile</p>"
      s += "<p>Here is the compiler output:</p>"
      F = open("./compilerErrors.txt","r")
      text = F.read()
      F.close()
      s += "<p>"+re.sub("\n","<p></p>",text)+"</p>"
      return s
    elif (correct==-2):
      s += "Your program was unsafe and contained a system call"
      return s
    else:
      s += "<p>Your program's output was not correct</p>"
      s += "<p> Expected Output:</p>"
      s += expected
      s += "<p> Student Output:</p>"
      s += received
    s += "<p>Your program took "+str(time)+" second"+"s"*(time!=1) +"  to run</p>"
    s += "<p>Your program consumed "+str(memory)+" byte"+"s"*(memory!=1)+" of memory</p>"
    return s

  def getSender(self,id):
    resp, data = self.conn.fetch(id,"(RFC822)")
    msg = data[0][1]
    ind = msg.find("From: ")
    return msg[msg.find("<",ind)+1:msg.find(">",ind)]

  def plz(singular,plural,num):
    if num == 1:
      return plural
    return singular

  def getAttachment(self,id,name):
    detach_dir = './code/'

    resp, data = self.conn.fetch(id, "(RFC822)") 
    email_body = data[0][1] 
    mail = email.message_from_string(email_body) 
    temp = self.conn.store(id,'+FLAGS', '\\Seen')
    self.conn.expunge()

    if mail.get_content_maintype() != 'multipart':
      self.current=None

    for part in mail.walk():
      if part.get_content_maintype() == 'multipart':
        continue
      if part.get('Content-Disposition') is None:
        continue

      filename = name+"_"+part.get_filename()
      att_path = os.path.join(detach_dir, filename)

      fp = open(att_path, 'wb')
      fp.write(part.get_payload(decode=True))
      fp.close()
      self.current = mail
      return part.get_filename()
    print name, "No Attachment"
    self.current = None

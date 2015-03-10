#!/usr/bin/python
# Purpose: send email notifications when autobuild finds build errors
# Usage: 1st argument is a quoted *string* to use as the subject of the email
#        2nd argument is a *file* to use as the body of the email.

import smtplib, string, sys, time, platform

if len(sys.argv) != 3:
    print "%s must be called with 2 arguments (a subject string and a filename for the body)" % sys.argv[0]
    sys.exit(1)

title = sys.argv[1]
filename = sys.argv[2]
infile = file(filename,'r')
content = infile.read()

arch = platform.processor()

server = smtplib.SMTP("host.domain.com")

From = arch + "@domain.com"
From = string.strip(From)
Date = time.ctime(time.time())
Subject = string.strip(title)
Text = string.strip(content)
To = []

##############################
##### List of Recipients #####
##############################

To.append("admin@domain.com")

##############################

Tostring = ",".join(To)
Tostring = string.strip(Tostring)
Header = ("From %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % (From, Tostring, Date, Subject))
smtp_result = server.sendmail(From, To, Header + Text)
server.quit()

if smtp_result:
    errstr = ""
    for recip in smtp_result.keys():
        errstr = """Could not delivery mail to: %s
Server said: %s
%s
%s""" % (recip, smtp_result[recip][0], smtp_result[recip][1], errstr)
    print smtplib.SMTPException, errstr
    sys.exit(1)
else:
    sys.exit(0)


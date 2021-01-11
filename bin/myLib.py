# RED = "\033[1;31;200m"
# YELLOW = '\033[1;32;200m'

import os

def reverse(str):
    return str[::-1]


def endsWith(haystack, needle):
    if needle in haystack:
        return reverse(haystack).index(reverse(needle)) == 0
    else:
        return False


def setParams(filename):
    with open(filename) as file:
        for line in file:
            #print("line=", line)
            if line.lstrip().startswith('#'):
                continue
            if line.lstrip().startswith('//'):
                continue
            if line.lstrip().replace(chr(10), "") == "":
                continue
            try:
                key, value = line.strip().split('=', 1)
            except:
                raise Exception("An error occurred reading parameters from filename, " + filename + ".  Line the failed:" + line)
            os.environ[key] = value


def colorString(str, color):
    if color is None:
        return str
    else:
        return color+ str + '\033[1;37;200m'


def factorial(num):
    if num != 0:
        fact = factorial(num-1)
    else:
        return 1

print(factorial(5))

def sendEmail(receivers, subject, body, filename=None, sender="herpintech@gmail.com"):
	import smtplib

	# import the corresponding modules
	from email import encoders
	from email.mime.base import MIMEBase
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	login = "herpintech@gmail.com"
	password = "Password=this1"

	sender_email = sender
	receiver_email = ",".join(receivers)

	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	# Open PDF file in binary mode

	# We assume that the file is in the directory where you run your Python script from
	if filename is not None:
		with open(filename, "rb") as attachment:
			# The content type "application/octet-stream" means that a MIME attachment is a binary file
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())

		# Encode to base64
		encoders.encode_base64(part)

		# Add header 
		part.add_header(
			"Content-Disposition",
			f"attachment; filename= {filename}",
		)

		# Add attachment to your message and convert it to string
		message.attach(part)
	text = message.as_string()

	# send your email
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(login, password)
	server.login(login, password)
	server.sendmail(
		sender_email, receiver_email, text
	)
	print('Email sent.') 
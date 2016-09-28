import smtplib

host = '*****'
key = '*****'
dest = '*******@sms.rogers.com'
msg = 'Subject: So long.\nDear Alice, so long and thanks for all the fish. Sincerely, Bob'

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()

smtpObj.starttls()
smtpObj.login(host, key)

smtpObj.sendmail(host, dest, msg)

smtpObj.quit()

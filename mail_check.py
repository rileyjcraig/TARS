import imapclient
import pyzmail

acc = '******'
key = '******'

imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
imapObj.login(acc, key)

imapObj.select_folder('INBOX', readonly = False)
UIDs = imapObj.search('UNSEEN')
rawMessages = imapObj.fetch(UIDs, ['BODY[]'])

while UIDs != []:
	#read oldest cmd first
	message = pyzmail.PyzMessage.factory(rawMessages[UIDs[-1]]['BODY[]'])
	print str(message.get_addresses('from')[0][0])	
	if message.text_part != None:
		body = message.text_part.get_payload().decode()
		cmd = str(body.split('\r\n')[1])
		print cmd, '\n'

	
	#pop oldest cmd
	UIDs.pop()

		

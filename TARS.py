import imapclient
import pyzmail
import smtplib
import pyautogui, time

host = 'projtars@gmail.com'
key = '******'

#initialise data in stream
data = ""

#for now destination is always my phone
dest = '********@sms.rogers.com'

#IMAP log-in
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
imapObj.login(host, key)

#SMTP log-in
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(host, key)

#print "all log ins done"

def save_print():
        global data
        #save page
        pyautogui.press('p')
        pyautogui.press('1')
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl', 'u')
        pyautogui.typewrite("output.txt")
        pyautogui.press('enter')
        pyautogui.press('y')
                
        #print first 150 characters
        file = open('output.txt', 'r')
        data = file.read()
        file.close()
        msg = data[0:150]
        send_msg(msg)
        data = data[150:]
        

def send_msg(msg):
        msg = 'Subject: TARS\n\n' + msg
        smtpObj.sendmail(host, dest, msg)


def exe_cmd(cmd, query):        #execute command, get output from lynx and forward to dest
        global data     #keep updating data left in stream
        cmd = cmd.lower()

        if cmd == 'hey' and query.lower() == 'tars':    #Welcome msg
                send_msg("Welcome! Enter 'h' for help.\n\nCurrent Personality Settings:\nHonesty: 95%\nHumour: 75%")

        elif cmd == 'h':        #help
                send_msg("List of Commands:\ng www.____.com - Enter a URL\n# query - Field# and query to search\n# - Link# to open link\ne - Enter\nr - Refresh page\nm - See more (scroll down page)\nj - Back\nk - Forward\nd - Debugging\nh - Help\nbye - Exit")
        elif cmd == 'd':
                send_msg("Advanced Debug Commands:\np - Print data to output stream\npk _key_ - Press key\ntw _string_ - Typewrite string\nkd _key_ - Key down\nku _key_ - Key up\n")

        elif cmd == 'g':        #URL
                pyautogui.press('g')
                pyautogui.typewrite(query)
                pyautogui.press('enter')

                time.sleep(5)
                save_print()
        
        elif cmd == 'm':        #send more data from stream     
                msg = data[0:150]
                send_msg(msg)
                data = data[150:]
        
        elif cmd.isdigit():     #LINK and FIELD QUERY...check if command is a non-negative integer; if so, open link
                pyautogui.typewrite(cmd)
                pyautogui.press('enter')
                #add an extra right arrow to activate button presses; shoudln't affect links...hopefully
                pyautogui.press('right') 
		            
                #if query, enter it into field
                if query != "":
                        #***remember to clear old text***
                        pyautogui.hotkey('ctrl', 'u')
                        pyautogui.typewrite(query)
                        pyautogui.press('enter')
        
                else:   #save and print newly opened link
                        time.sleep(5)
                        save_print()    
        
        elif cmd == 'e':        #enter
                        pyautogui.press('enter')
                        time.sleep(5)
			save_print()
        

        elif cmd == 'p':        #Print
                save_print()    
        
        elif cmd == 'r':        #Refresh
                pyautogui.hotkey('ctrl', 'l')
                save_print()

        elif cmd == 'j':        #Go back
                pyautogui.press('left')
                save_print()

        elif cmd == 'k':        #Go forward
                pyautogui.press('right')
                timer.sleep(5)	#forward opens a new link; takes some time
		save_print()
        
        elif cmd == 'bye':      #terminate and restart
                send_msg("Self destruct sequence in T minus 10, 9, 8...")
                send_msg("...1...")
        
                pyautogui.hotkey('ctrl', 'c')   #kill lynx
                
                #logout and exit (only to be restarted by bash script)
                imapObj.logout()
                smtpObj.quit()
                exit

        #Debugging Commands
        elif cmd == 'pk':
                pyautogui.press(query)
        elif cmd == 'tw':
                pyautogui.typewrite(query)
        elif cmd == 'kd':
                pyautogui.keyDown(query)
        elif cmd == 'ku;':
                pyautogui.keyUp(query)

        else:
                send_msg("Invalid Command.")


#print "reached right before loop"
#while in-session, keep looking for new cmds
while True:
        #print "started loop"
        imapObj.select_folder('INBOX', readonly = False)
        UIDs = imapObj.search('UNSEEN')
        rawMessages = imapObj.fetch(UIDs, ['BODY[]'])
        #print "UIDs", UIDs, "reached after raw msgs"
        while UIDs != []:
                
                #read oldest cmd first
                message = pyzmail.PyzMessage.factory(rawMessages[UIDs[-1]]['BODY[]'])
                        
                if message.text_part != None:
                        body = message.text_part.get_payload().decode()
                                
                        #separate user-entered text from entire body
                        txt = str(body.split('\r\n')[0])

                        #partition text into command and query (separated by a space; ignore space)
                        txt_list = txt.partition(" ")
                        cmd = txt_list[0]
                        query = txt_list[2]
                        #print "body&text&cmd&query:", body, txt, cmd, query
                        #execute cmd
                        exe_cmd(cmd, query)
                #pop oldest cmd
                UIDs.pop()


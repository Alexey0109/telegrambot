import requests
import json
import time

_TOKEN_ = '959976424:AAHQ7FxDWp9kCiRJjCwoj4EOnMQTwDshOsU'

def sendRequest(method):
    url = 'https://api.telegram.org/bot' + _TOKEN_ + '/'
    #print(url + method)
    response = requests.get(url + method)
    #print(response.text)
    return response

def sendMessage(ID, msg):
    sendRequest('sendMessage?chat_id='+ID+'&text='+msg)
    print('Sending message: ' + msg)

def getUpdates():
    update = sendRequest('getUpdates')
    r = json.loads(update.text)
    return r

def messages(text, chat_id):
    if(text == '/start'):
        sendMessage(chat_id, 'Starting...')
    elif(text == '/stop'):
        sendMessage(chat_id, 'Stopping...')
    elif(text == '/help'):
        sendMessage(chat_id, 'Help')
    else:
        msgfile = open('messages.txt', 'r')
        reply = open('replies.txt', 'r')
        num = 0
        rtext = ''
        for num, line in enumerate(msgfile, 1):
            if text.lower() in line.lower():
                reply = open('replies.txt', 'r')
                rtext = ''
                for j in range(num):
                    rtext = reply.readline()
                sendMessage(chat_id, rtext)
                print(rtext)
                reply.close()
        msgfile.close()

def addMessage(chat_id, prev):
    sendMessage(chat_id, 'Enter message: ')
    while(True):
        r = getUpdates()['result'][-1]['message']
        if(int(r['message_id']) != prev):
            prev = int(r['message_id'])
            #print(prev_id)
            msg = r['text']
            msgfile = open('messages.txt', 'a')
            msgfile.write(msg + '\n')
            msgfile.close()
            break
    sendMessage(chat_id, 'Enter reply: ')
    while(True):
        r = getUpdates()['result'][-1]['message']
        if(int(r['message_id']) != prev):
            prev = int(r['message_id'])
            #print(prev_id)
            msg = r['text']
            msgfile = open('replies.txt', 'a')
            msgfile.write(msg + '\n')
            msgfile.close()
            break
    sendMessage(chat_id, 'Succeed!')
prev_id = 0

while(True):
    r = getUpdates()['result'][-1]['message']
    if(int(r['message_id']) != prev_id):
        print(str(r['chat']['id']) + ' ' + r['text'], end='; ')
        prev_id= int(r['message_id'])
        print(prev_id)
        if (r['text'] == '/add_message'):
            addMessage(str(r['chat']['id']), int(prev_id))
        else:
            messages(r['text'], str(r['chat']['id']))
    #time.sleep(2.5)
print('End')
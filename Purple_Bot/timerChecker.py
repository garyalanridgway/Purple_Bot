import time
import pollAndPlace
import textUpdates

#create the config dict
config ={}
with open('config.txt','r') as cFile:
    for line in cFile:
        line = line.strip().split(':')
        config[line[0]] = int(line[1])
        

#gets the current time and returns a list [int, int] of [Hour, Minute]
##def getTime():
##    return([int(HM) for HM in time.strftime('%H,%M').split(',')])

#global variables
masterLock =True
keywords=['bigRestart']
passes=0
polls=0
pingsT=0

##def tryStart():
##    #try to log in, if you are already logged in, dont log in
##    try:
##        textUpdates.startUp()
##    except:
##        pass
##    try:
##        textUpdates.connect()
##    except:
##        pass
    
def eTimeCheck():
    global config
    ctime =[int(HM) for HM in time.strftime('%H,%M').split(',')]
    return((ctime[0]%2==config['Hour']) and (ctime[1]==config['Minute']) )

def tryPollAll():
    global masterLock
    global keywords
    global passes
    global polls
    global pingsT
    #try to poll /r/all
    print('Trying to poll /r/all...')
    try:
        pollAndPlace.pollAll()
        polls+=1
        print('Completed a Poll of /r/all...')
        #problem child vvvvvvvv
        #textUpdates.textUser('Completed a Poll of /r/all\nTotal Polls : '+str(polls))
    except Exception as e:
        textUpdates.textUser('Could not poll /r/all.\n\n'+str(e)[:50])
    
def runnit():
    global masterLock
    global keywords
    global passes
    global polls
    global pingsT
    #textUpdates.startUp()
    textUpdates.textUser('Starting Up')
    print('Starting up...')
    try:
        while masterLock:
            #tryStart()
            print('Pass '+str(passes)+' of this Round')
            passes+=1
            print('Running Minute check...')
            bigBreak=False
            #if it is a certain time of day, do a poll and place
            print('Checking Time...')
            print(str(time.strftime('%H:%M:%S')))
            if eTimeCheck():
                tryPollAll()
            #try to process emails and set the new keywords list. if there were no keywords,
            #it will be set to empty again
            print('Trying to process emails...')
            try:
                #tryStart()
                keywords=textUpdates.processEmails()
            except Exception as e:
                textUpdates.textUser('keywords failed to execute, will not be able to process any further commands until this is physically resolved.\n\n'+str(e)[:50])
                break
            print('Trying to execute keywords...')
            for key in keywords:
                if key == 'masterlock-stop':
                    print('**')
                    print('keyword "masterlock-stop" found')
                    print('**')
                    masterLock=False
                if key == 'ping':
                    print('**')
                    print('keyword "ping" found')
                    print('**')
                    pingsT+=1
                    textUpdates.textUser('System is still online\nTotal Passes :'+str(passes)+'\nTotal Polls : '+str(polls)+'\nTotal Pings :'+str(pingsT))
                if key == 'force-poll':
                    print('**')
                    print('keyword "force-poll" found')
                    print('**')
                    tryPollAll()
                if key == 'restart':
                    print('**')
                    print('keyword "restart" found')
                    print('**')
                    keywords =['bigRestart']
                    bigBreak = True
                    break
            if bigBreak:
                break
            #wait 60 secods between anything
            print('Trying to sleep...')
            print('_______________________________________')
            try:
                time.sleep(60)
            except Exception as e:
                textUpdates.textUser('the time module is not functioning properly\n\n'+str(e)[:50])
                break

        
        
    except Exception as e:
        textUpdates.textUser('Something HORRIBLY WRONG has happened, program has ended.\n\n'+str(e)[:50])
        #textUpdates.closeOut()
while 'bigRestart' in keywords:
    runnit()
    textUpdates.textUser('Shutting Down')
    print('Shutting Down...')
#textUpdates.closeOut()

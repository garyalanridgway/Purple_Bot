import praw
import time
import unicodedata

#create the config dict
config ={}
with open('config.txt','r') as cFile:
    for line in cFile:
        line = line.strip().split(':')
        config[line[0]] = int(line[1])

bot = praw.Reddit(user_agent='Purple_Bot v1.0',
                  client_id='7zq-i3CnuSYeTQ',
                  client_secret='UyMd9wVqYZ5Ues_TnLr9ehX45ek',
                  username='Purple_Bot',
                  password='purplemango1234')
subreddit = bot.subreddit('all')

#polls "numPosts" posts from /r/all and puts all of that in to a dated csv file
numPosts = config['NumPosts']
def normalize(text):
    return((''.join(c for c in unicodedata.normalize('NFC', text) if c <= '\uFFFF')).lstrip())

def pollAll():
    global non_bmp_map
    dDict = {}
    #creates the dictionary out of the current file to save entries that
    #are no longer in the top "numPosts" posts
    try:
        with open('data//'+str(time.strftime("%d-%m-%Y"))+'.csv','r')as wFile:
            count = 0
            for line in wFile:
                if count == 0:
                    count+=1
                else:
                    line = normalize(line)
                    line = line.strip().split(",")
                    dDict[line[0].strip(',')]=[line[1],line[2],line[3],line[4]]
    except:
        #if the file for the day does not exist, create it
        open('data//'+str(time.strftime("%d-%m-%Y"))+'.csv','w')
    #now take the current "numPost" posts at the top of /r/all's "hot" section,
    #and add them to the day's dictionary
    for submission in subreddit.hot(limit=numPosts):
            dDict[normalize(str(submission.title))] = [normalize(str(submission.subreddit)),normalize(str(submission.author)),int(submission.score),len(submission.comments.list())]
            #print(dDict[submission.title])
    #now output them to the file of the day
    with open('data//'+str(time.strftime("%d-%m-%Y"))+'.csv','w') as wFile:
        wFile.write("Title,Subreddit,Author,Score,Comments\n")
        for entry in dDict:
            wFile.write(entry+','+str(dDict[entry][0])+','+str(dDict[entry][1])+','+str(dDict[entry][2])+','+str(dDict[entry][3])+'\n')

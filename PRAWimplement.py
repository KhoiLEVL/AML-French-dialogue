import praw
import numpy as np
from statistics import mode
target_subreddit = "france"
final = {}
conversation = {}
finalconvo = []


def getall(comment):
    if len(comment.replies) != 0:
        for reply in comment.replies:
            allcomments.append(reply)
            getall(reply)

def traverse(temparray, targetarray, origcomm, submis):
    for i in range(0,len(temparray)):

        if(temparray[i].parent() == comm):

            targetarray.append(comm.body)
            targetarray.append(temparray[i].body)

            for j in range(i+1, len(temparray)):
                if (((temparray[j].parent() == temparray[j-1].parent()) or (temparray[j].parent() == temparray[j-1])) and (temparray[j].parent() != comm) and (j!=len(temparray)-1)):
                    targetarray.append(temparray[j].body)
                else:
                    finalconvo.append(targetarray)
                    targetarray = []
                    break
        else:
            continue

reddit = praw.Reddit(client_id='tj8tNHMaV41yVQ',
                     client_secret='z-ER9Q4zlxnT7-gqbhd9Bjr8JeQ',
                     user_agent='Dialoguemaker')

subreddit = reddit.subreddit(target_subreddit)

dialogue1 = []
heading = {}
subcount = 0

for submission in subreddit.hot(limit = 1):
    subcount = subcount + 1
    print(subcount)
    allcomments = []
    dialogue1.append(submission.title)
    submission.comments.replace_more(limit=None)
    submission.comment_sort='best'
    topcomments = list(submission.comments)

    for comment in topcomments:
        allcomments.append(comment)
        getall(comment)

    final.update({submission.title:allcomments})

    newdict = {}
    tracker = 0
    for count in range(len(allcomments)):
        if (allcomments[count] in topcomments):
            temp =[]
            tracker = count+1
            for counter in range(tracker, len(allcomments)):
                if (allcomments[counter] in topcomments):
                    break
                else:
                    temp.append(allcomments[counter])
            newdict.update({allcomments[count]:temp})


    for comm in topcomments:
        convo = []
        parentcomm = []
        temp = newdict[comm]

        if len(temp)>0:
            if len(temp)==1:
                convo.append(comm.body)
                convo.append(temp[0].body)
                finalconvo.append(convo)
                continue
            else:
                traverse(temp, convo, comm, submission)

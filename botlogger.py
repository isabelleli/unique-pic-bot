import os
from datetime import datetime

def logwrite(message):
    with open(logFileName, 'a') as f:
        timeElapsed = datetime.now() - logStartTime
        timedMsg = str(timeElapsed) + ': ' + message 
        f.write(timedMsg + "\n")

def createLogFile():
    global logFileName
    global logStartTime
    if not os.path.exists("logfiles"):
        os.mkdir("logfiles")
    logStartTime = datetime.now()
    startTimeString = logStartTime.strftime("%Y-%m-%d %H-%M-%S")    
    logFileName = 'logfiles/' + startTimeString + '.txt'


   
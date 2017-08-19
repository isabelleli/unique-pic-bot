import praw
from praw.exceptions import APIException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import requests
import time
from botlogger import createLogFile, logwrite
import sys

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://tineye.com')        

def comment(submission, matches, postList, submissionID, logMessage):
    try:
        submission.reply("There are " + str(matches) + " pictures of this pet on the internet." + 
        "(unless your pet is internet famous b/c in that case please introduce me to them ;) )")
        postList.append(submissionID)
        logwrite(logMessage)
    except APIException as err:
        time.sleep(360) #last time, API throttled by requiring a wait-time of 6 minutes
        logwrite("Hey, you got an APIException! Recursively calling the comment function")
        comment(submission, matches, postList, submissionID, "You got a APIException but you commented on this post!")

def sendURL(url):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'url_box'))) 
        url_box = driver.find_element_by_id('url_box')
        url_box.send_keys(url)
        url_box.submit()
    except TimeoutException as err:
        logwrite(err + ' Used up to tineye searching limits. Quitting program')
        sys.exit()
        
    
def reverseSearch(subredditName):
    createLogFile()
    r = praw.Reddit('bot1')
    subreddit=r.subreddit(subredditName)
    urls = []
    logwrite("Crawling through " + subredditName)
    
    for submission in subreddit.hot(limit=20):
        req = requests.get(submission.url)
        if 'image' in req.headers['content-type']: #checks to make sure it's an image
            urls.append((submission.id, submission.url))
            
    logwrite("Checked 10 submissions. There are " + str(len(urls)) + " images")
    fName = 'responded_posts/'+subredditName+'.txt' #file contains ID's of submission posts that the bot has already commented on
    responded_posts = []
    if os.path.isfile(fName):
        with open(fName) as f:
            content = f.readlines()
        responded_posts = [line.strip() for line in content]
    
    for url in urls:
        sendURL(url[1])
        try:
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'h2'))
            WebDriverWait(driver, 5).until(element_present) #waits 5 seconds to throw TimeoutException unless it finds element to return 
            results = driver.find_element_by_tag_name('h2') #result usually looks like "# Results"
            if 'result' not in results.text.lower():
                logwrite('Used up tineye searching limits. Quitting program')
                sys.exit()
            matches = int(results.text.split(' ')[0])
            logwrite('got a match - here it is: ' + str(matches))
            if matches > 4 and url[0] not in responded_posts:
                logwrite("Found non-unique picture! There are " + str(matches) + " matches")
                submission = r.submission(id=url[0])
                comment(submission, matches, responded_posts, url[0], "A comment has been posted!")
        except TimeoutException as err:
            logwrite(err)
        except NoSuchElementException as err:
            logwrite(err)
        
        time.sleep(3)
        
    with open(fName, 'w') as f:
        for post in responded_posts:
            f.write(post + '\n')
    
    logwrite("Finished")
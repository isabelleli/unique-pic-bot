# unique-pic-bot

A bot that identifies whether images (specifically animal pictures) are unique by using Tineye's reverse image search and posts a comment **if** the picture isn't unique.

# Getting Started

I'm using Python 3.6.1 to run this bot. I'm also using: 

- PRAW (Python Reddit API Wrapper) to easily access Reddit's API. 
```
pip install praw
```

- Selenium to reverse image search on tineye.com
```
pip install -U selenium
```

- Requests (HTTP library) to get the content type of a reddit post's submitted url and verify that it's an image
```
pip install requests
```

# Uses

This bot was originally intended for r/aww since there are often reposts of the same animal pictures. However, they don't allow bots in their subreddit. This bot could be used in any other animal subreddit and the comment posted by the bot could be easily changed to apply to any subreddit that is image-based.

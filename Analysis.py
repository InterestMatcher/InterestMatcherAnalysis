# Author: Will Robbins, Tommy Yu
import requests
import json
import pprint
import unicodedata
import smtplib
import getpass
from email.mime.text import MIMEText
from firebaseSecret import AUTHSECRET
from alchemyapi import AlchemyAPI

# Toggle this for development/debug mode
DEV_MODE = True

chatsUrl = "https://interestmatcher.firebaseio.com/chatrooms/public.json"
postsUrl = "https://interestmatcher.firebaseio.com/posts/chill.json"

def get_chat_content():
	chats = []
	r1 = requests.get(chatsUrl + "?print=pretty" + "&auth=" + AUTHSECRET)
	chatData = json.loads(r1.text) # JSON of all the chats
	for chatContent in chatData.values():
		converted = ""
		converted = unicodedata.normalize('NFKD', chatContent["content"]).encode('ascii', 'ignore')
		chats.append(converted)
	return chats

def get_post_content():
	posts = []
	r2 = requests.get(postsUrl + "?print=pretty" + "&auth=" + AUTHSECRET)
	postData = json.loads(r2.text) # JSON of all the posts
	for postContent in postData.values():
		converted = ""
		converted = unicodedata.normalize('NFKD', postContent["content"]).encode('ascii', 'ignore')
		posts.append(converted)
	return posts

def keywords_and_sentiment(contentList):
	# Accepts a string of posts (or chats), and returns a list of keywords
	alchemyapi = AlchemyAPI()
	relevanceList = []
	sentiment = 0
	counter = 0

	for post_message in contentList:
		response = alchemyapi.keywords('text', post_message, {'sentiment': 1})
		if response['status'] == 'OK':
			for keyword in response['keywords']:
				if 'score' in keyword['sentiment']:
					sentiment += float(keyword['sentiment']['score'])
				if float(keyword['relevance']) > .97:
					relevanceList.append(keyword['text'])
				counter += 1
	if DEV_MODE:
		if not counter is 0:
			print float(sentiment/counter)

	return relevanceList

def send_digest_email(username, password, recipient):
	# Accepts strings with the address & password of an email account (IMAP/SMTP enabled) 
	# and send email to recipient email address

	text = "Hello!  This is your Interest Matcher Email Digest.  " + \
		"Here are things people have been talking about:\n" + str(keywords_and_sentiment(get_post_content()))

	if DEV_MODE:
		print text

	# Send the message
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(username, password)
	server.sendmail(username, recipient, text)
	server.quit()

# Play around with this in testing - only runs in development mode
if DEV_MODE:
	pprint.pprint(get_chat_content()) 
	print '\n'

	pprint.pprint(get_post_content())
	print '\n'

	print keywords_and_sentiment(get_post_content())
	print '\n'

	# NOTE! To login to gmail through IMAP/SMTP, you must enable "less secure apps" in your gmail settings.
	print "enter sending gmail username: "
	addr = str(raw_input()) + "@gmail.com"
	print "enter password"
	pw = str(getpass.getpass())
	print "enter recipient email address: "
	recip = str(raw_input())
	send_digest_email(addr, pw, recip)






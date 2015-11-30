import requests
import json
import pprint
from firebaseSecret import AUTHSECRET
from alchemyapi import AlchemyAPI

# Toggle this for development/debug mode
DEV_MODE = True

chatsUrl = "https://interestmatcher.firebaseio.com/chatrooms/public.json"
postsUrl = "https://interestmatcher.firebaseio.com/posts/chill.json"

def get_chat_content():
	chats = []
	r1 = requests.get(chatsUrl + "?print=pretty" + "?auth=" + AUTHSECRET)
	chatData = json.loads(r1.text) # JSON of all the chats
	for chatContent in chatData.values():
		chats.append(chatContent["content"])
	return chats

def get_post_content():
	posts = []
	r2 = requests.get(postsUrl + "?print=pretty" + "?auth=" + AUTHSECRET)
	postData = json.loads(r2.text) # JSON of all the posts
	for postContent in postData.values():
		posts.append(postContent["content"])
	return posts

def keywords_and_sentiment(contentList):
	# Accepts a string of posts (or chats), and returns a dictionary with keywords and sentiment
	alchemyapi = AlchemyAPI()
	relevanceList = []
	sentiment = 0
	counter = 0

	for post_message in contentList:
		response = alchemyapi.keywords('text', post_message, {'sentiment': 1})
		if response['status'] == 'OK':
			for keyword in response['keywords']:
				print keyword
				sentiment += float(keyword['sentiment']['score'])
				counter += 1
		else:
			return 'Error: ' + response['statusInfo']

	return float(sentiment/counter)


# Play around with this in testing - only runs in development mode
if DEV_MODE:
	pprint.pprint(get_chat_content()) 
	print '\n'
	pprint.pprint(get_post_content())
	print '\n'
	print keywords_and_sentiment(get_post_content())
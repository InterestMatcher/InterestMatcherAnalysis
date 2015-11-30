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

def convert_to_pure_text(content):
	# Takes a list (posts or chats) and removes non-english things for alchemy to work with
	#content = [ "u\'Anyone wanna Netflix and Chill?\'", "u\'broken af\'"]
	formatted = str()
	for post in content:
		#post = str(post)
		post = ''.join(chr(ord(c)) for c in post)
		formatted += post#[2:len(post)-1] # Firebase gives posts in format:  u'Post Content Here!'
	print formatted
	return formatted

def keywords_and_sentiment(text):
	# Accepts a string of posts (or chats), and returns a dictionary with keywords and sentiment
	alchemyapi = AlchemyAPI()
	response = alchemyapi.keywords('text', text, {'sentiment': 1})
	output = str()

	if response['status'] == 'OK':
		print response['keywords']
		for keyword in response['keywords']:
			output += 'text: ' + keyword['text'].encode('utf-8') + " \n"
			output += 'relevance: ' + keyword['relevance'] + " \n"
			output += 'sentiment: ' + keyword['sentiment']['type'] + " \n"
			# This throws an error for some reason.
	        #if 'score' in keyword['sentiment']:
	        #    output += 'sentiment score: ' + keyword['sentiment']['score']
	else:
		return 'Error! ' + response['statusInfo']

	return output


# Play around with this in testing - only runs in development mode
if DEV_MODE:
	pprint.pprint(get_chat_content()) 
	print '\n'
	pprint.pprint(get_post_content())
	print '\n'
	print keywords_and_sentiment(convert_to_pure_text(get_post_content()))
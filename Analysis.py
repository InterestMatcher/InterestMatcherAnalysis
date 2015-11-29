import requests
import json
from firebaseSecret import AUTHSECRET

chatsUrl = "https://interestmatcher.firebaseio.com/chatrooms/public.json"
postsUrl = "https://interestmatcher.firebaseio.com/posts/chill.json"

#Get Chat messages
r1 = requests.get(chatsUrl + "?print=pretty" + "?auth=" + AUTHSECRET)
chatData = json.loads(r1.text) #JSON of all the chats
chats = [] #List of all the chat messages

for chatContent in chatData.values():
	chats.append(chatContent["content"])

print chats #Debugging purposes only
print '\n'

#Get Post content
r2 = requests.get(postsUrl + "?print=pretty" + "?auth=" + AUTHSECRET)
postData = json.loads(r2.text) #JSON of all the posts
posts = [] #List of all the post content

for postContent in postData.values():
	posts.append(postContent["content"])

print posts #Debugging purposes only



import requests
import json
from firebaseSecret import AUTHSECRET

postsUrl = "https://interestmatcher.firebaseio.com/chatrooms/public.json"

r = requests.get(postsUrl + "?print=pretty" + "?auth=" + AUTHSECRET)
postData = json.loads(r.text) #JSON of all the posts
posts = [] #Array of all the post content

for postContent in postData.values():
	posts.append(postContent["content"])

print posts #Debugging purposes only

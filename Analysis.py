import requests
import json
from firebaseSecret import AUTHSECRET

postsUrl = "https://interestmatcher.firebaseio.com/chatrooms/public.json"

r = requests.get(postsUrl + "?print=pretty" + "?auth=" + AUTHSECRET)
postData = json.dumps(json.loads(r.text), indent=4, sort_keys=True) #JSON of all the posts
print postData #Debugging purposes only

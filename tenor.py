import requests
import json
import os

# set the apikey and limit
apikey = os.environ['TENOR_KEY']  # click to set to your apikey
# lmt = 8
ckey = "my_test_app"  # set the client_key for the integration and use the same value for all API calls

def search_tenor(search_term, lmt):
    # our test search
    
    # get the top 8 GIFs for the search term
    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))
    
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
        #print(top_8gifs)
        #print("-------------")
        #print(top_8gifs['results'][0]['media_formats']['tinygif']['url'])
    else:
        top_8gifs = None
        
    return top_8gifs

search_tenor("emotional damage", 1)
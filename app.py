import flask
import json
import urllib.parse
import os
import requests
app = flask.Flask(__name__)

subscriptionKey = os.getenv("subscriptionKey")
endpoint = 'https://api.bing.microsoft.com'
customConfigId = 'e5f9a53e-48fa-4b66-9d43-9b52fb158d18'

@app.route('/')
def index():
    if query := flask.request.args.get('query'):
        return flask.redirect(f"/{query}")
    return "Welcome to pdork V2. Supply a query to get a new site." +\
           "<form action=\"/\">" +\
           "<input type=\"text\" id=\"query\" name=\"query\">" +\
           "<input type=\"submit\" value=\"Submit\"><br><br>" +\
           "What am I looking at? <br> "+\
            "- This site bing dorks pastebin for your query plus the term &lt!DOCTYPE html&gt "+\
           "and returns the first result as a webpage <br>" +\
            "Why? <br>"+\
            "- V1 was a project for RITSEC. It was an exploration of pastebin dorking, including finding crypto private"+\
           "keys, phishing, seo, and more chaos. Unfortunately, the recording has no sound. <br>"+\
            "What's new in V2?<br>" +\
            "- V2 cleans up some dangling unfinished features and makes the website spiderable.<br><br><br>"+\
            "Find me on <br> <a href=https://github.com/secureighty>github</a> <br>"+\
           "<a href=https://www.linkedin.com/in/secureighty/>linkedin</a><br>"+\
           "<a href=https://twitter.com/Secureighty>twitter</a><br>"



@app.route('/<path:query>')
def site(query):
    return get_site(query)

def get_site(query):
    global subscriptionKey
    global customConfigId
    global endpoint
    searchTerm = urllib.parse.quote_plus("site:pastebin.com <!DOCTYPE html> " + query)
    resp = requests.get(f"{endpoint}/v7.0/custom/search?q={searchTerm}%20&customconfig={customConfigId}&mkt=en-US", headers={"Ocp-Apim-Subscription-Key":subscriptionKey})
    searchresult = resp.json()
    firsturl = searchresult["webPages"]["value"][0]["url"]
    firsturl = firsturl[:20]+'/raw'+firsturl[20:]

    rawtext=requests.get(firsturl).text
    return rawtext

app.run()


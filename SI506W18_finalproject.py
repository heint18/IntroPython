#Author: Tyler Hein

#SI 506 Final Project, Option 1

#Import statements
import requests
import requests_oauthlib
import webbrowser
import json
import string
import twitter_credentials

#Setting up the cache for twitter and itunes data
CACHE_FNAME = "SI506W18finalproject_cache.json"
try:
    f = open(CACHE_FNAME, 'r')
    f_string = f.read()
    f.close()
    CACHE_DICTIONARY = json.loads(f_string)
except:
    CACHE_DICTIONARY = {}

#Setting up Twitter credentials - see README.txt and twitter_credentials.py for more information
client_key = twitter_credentials.consumer_key
client_secret = twitter_credentials.consumer_secret

if not client_secret or not client_key:
    print("You need to fill in client_key and client_secret")
    exit()

#Defining a function to get tokens for Twitter
def get_twitter_tokens():
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret = client_secret)
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    fetch_resp = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_resp.get('oauth_token')
    resource_owner_secret = fetch_resp.get('oauth_token_secret')
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)
    webbrowser.open(authorization_url)
    verifier = input('Please input the verifier: ')
    oauth = requests_oauthlib.OAuth1Session(client_key,
                                client_secret = client_secret,
                                resource_owner_key = resource_owner_key,
                                resource_owner_secret = resource_owner_secret,
                                verifier = verifier)
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

#Checking if there are cached credentials and get them if not
if "credentials" in CACHE_DICTIONARY:
    client_key, client_secret, resource_owner_key, resource_owner_secret, verifier = CACHE_DICTIONARY["credentials"]
else:
    twitter_tokens = get_twitter_tokens()
    client_key, client_secret, resource_owner_key, resource_owner_secret, verifier = twitter_tokens
    CACHE_DICTIONARY["credentials"] = twitter_tokens
    cache_dump = json.dumps(CACHE_DICTIONARY)
    f = open(CACHE_FNAME, 'w')
    f.write(cache_dump)
    f.close()

#Defining a function to create a unique identifier for each Twitter search
def twitter_params_unique_combination(baseurl, params_d, private_keys = ["api_key"]):
    sorted_keys = sorted(params_d.keys())
    twitter_results = []
    for key in sorted_keys:
        twitter_results.append("{}-{}".format(key, params_d[key]))
    return baseurl + "_".join(twitter_results)

#Defining a function to access at least 50 posts from Twitter, based on any search, either tweets from 1 specific public user (can't be protected) or by keyword search
#This function gets and caches data based on input, either input of a Twitter username or a search term
def twitter_get_cache_search(search_terms = None, user_search = None, num_results = 50):
    params_dictionary = {}
    if search_terms is not None:
        params_dictionary["q"] = search_terms
        base_url = "https://api.twitter.com/1.1/search/tweets.json"
        params_dictionary["count"] = num_results
    if user_search is not None:
        params_dictionary["screen_name"] = user_search
        base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params_dictionary["count"] = num_results
    twitter_unique_identifier = twitter_params_unique_combination(base_url, params_dictionary)
    if twitter_unique_identifier in CACHE_DICTIONARY:
        return CACHE_DICTIONARY[twitter_unique_identifier]
    else:
        oauth = requests_oauthlib.OAuth1Session(client_key,
                            client_secret=client_secret,
                            resource_owner_key=resource_owner_key,
                            resource_owner_secret=resource_owner_secret)
        resp = oauth.get(base_url, params= params_dictionary)
        twitter_data = resp.text
        twitter_dictionary = json.loads(resp.text)
        CACHE_DICTIONARY[twitter_unique_identifier] = twitter_dictionary
        cache_dump = json.dumps(CACHE_DICTIONARY)
        f = open(CACHE_FNAME, 'w')
        f.write(cache_dump)
        f.close()
        return CACHE_DICTIONARY[twitter_unique_identifier]

#Defining a function to create a unique identifier for each iTunes search
def iTunes_params_unique_combination(baseurl, params_d):
    sorted_keys = sorted(params_d.keys())
    itunes_results = []
    for key in sorted_keys:
        itunes_results.append("{}-{}".format(key, params_d[key]))
    return baseurl + "_".join(itunes_results)

#Defining a function that gets, caches, and returns data from the iTunes API for songs based on keyword search input
def itunes_get_cache_search(keyword):
    baseurl = "https://itunes.apple.com/search"
    params_dictionary = {}
    params_dictionary["term"] = keyword
    params_dictionary["entity"] = "song"
    iTunes_unique_identifier = iTunes_params_unique_combination(baseurl, params_dictionary)
    if iTunes_unique_identifier in CACHE_DICTIONARY:
        return CACHE_DICTIONARY[iTunes_unique_identifier]
    else:
        resp = requests.get(baseurl, params = params_dictionary)
        itunes_data = resp.text
        itunes_dictionary = json.loads(itunes_data)
        CACHE_DICTIONARY[iTunes_unique_identifier] = itunes_dictionary
        json_cache_dump = json.dumps(CACHE_DICTIONARY)
        f = open(CACHE_FNAME, 'w')
        f.write(json_cache_dump)
        f.close()
        return CACHE_DICTIONARY[iTunes_unique_identifier]

#Defining a class tweet
#Has a __str__ method that represents information about each tweet clearly
#Has one additional method should return the longest word in the tweet

class Tweet(object):
    def __init__(self, tweet_dictionary):
        self.text = tweet_dictionary["text"]
        self.username = tweet_dictionary["user"]["screen_name"]
        self.hashtags = tweet_dictionary["entities"]["hashtags"]

    def get_number_hashtags(self):
        number_hashtags = 0
        for hashtag in self.hashtags:
            number_hashtags = number_hashtags + 1
        return number_hashtags
#working well except now long spaces are sometimes the longest word...
    def get_longest_word(self):
        tweet_word_dictionary = {}
        s = self.text.replace(","," ")
        s = s.replace(": "," ")
        s = s.replace(";"," ")
        s = s.replace("-"," ")
        s = s.replace("..."," ")
        for word in s.split():
            char_list = list(word)
            if char_list[0] is "@":
                tweet_word_dictionary[word] = 0
            elif char_list[0] is "#":
                tweet_word_dictionary[word] = 0
            elif word.startswith("https"):
                tweet_word_dictionary[word] = 0
            elif word.startswith("RT"):
                tweet_word_dictionary[word] = 0
            else:
                word_lettersonly = ""
                for char in word:
                    if char in string.ascii_letters:
                        word_lettersonly = word_lettersonly + char
                tweet_word_dictionary[word_lettersonly] = len(word_lettersonly)
        longest_word_length = 0
        longest_word = ""
        for key in tweet_word_dictionary.keys():
            if tweet_word_dictionary[key] > longest_word_length:
                longest_word_length = tweet_word_dictionary[key]
                longest_word = key
        return longest_word

    def __str__(self):
        return "{} posted the following tweet: {}. It has {} hashtags and {} is the longest word in it.".format(self.username,self.text,self.get_number_hashtags(), self.get_longest_word())

#Defining a class Song
#Has a method to convert the song length in milliseconds to seconds

class Song(object):
    def __init__(self, song_dictionary):
        self.name = song_dictionary["trackName"]
        self.artist_name = song_dictionary["artistName"]
        self.trackTime = song_dictionary["trackTimeMillis"]

    def get_song_length_sec(self):
        song_length_ms = int(self.trackTime)
        song_length_sec = (song_length_ms/1000)
        return song_length_sec

    def __str__(self):
        return "{} is a song by {}. It is {} seconds long.".format(self.name,self.artist_name,self.get_song_length_sec())

#Invoking the function that gets data from Twitter, and ultimately create a list of instances of class Tweet
#Here, I have set it up such that you first enter whether you'd like to search by keyword or Username
#If you do not type in keyword or username, the rest of the program runs with a keyword search for mountains as an example
#Then, there is a second opportunity to input either keyword or Username

tweet_instances = []

twitter_search_type = input("Would you like to search by keyword or username?: ")
if twitter_search_type == "keyword":
    twitter_search_keyword = input("Please enter the keyword(s): ")
    twitter_data = twitter_get_cache_search(search_terms = twitter_search_keyword)
    for tweet_dictionary in twitter_data["statuses"]:
        t = Tweet(tweet_dictionary)
        tweet_instances.append(t)

elif twitter_search_type == "username":
    twitter_search_username = input("Please enter the username: ")
    twitter_data = twitter_get_cache_search(user_search = twitter_search_username)
    for tweet_dictionary in twitter_data:
        t = Tweet(tweet_dictionary)
        tweet_instances.append(t)
else:
    print("Sorry, that request is not valid. The program will continue running with the example of a keyword search for mountains.")
    twitter_data = twitter_get_cache_search(search_terms = "mountains")
    for tweet_dictionary in twitter_data["statuses"]:
        t = Tweet(tweet_dictionary)
        tweet_instances.append(t)

#Sorting the list of Tweet instances by how many hashtags they have

sorted_tweets = sorted(tweet_instances, key = lambda x: x.get_number_hashtags())
#testing sorted_tweets and invoking string method of class Tweet
for tweet in sorted_tweets:
    print(tweet)

#Creating an empty list to hold Song instances

song_instances = []

#For each Tweet instance in the sorted list of Tweet instances, invoking the function that makes a request to the iTunes API with the input of the longest word in that Tweet
#From the data from each request, creating a Song instance from the first song in the data and append it to a list of song instances

for tweet in sorted_tweets:
    try:
        songs_data = itunes_get_cache_search(tweet.get_longest_word())
        if songs_data["resultCount"] != 0:
            one_song_data = songs_data["results"][0]
            s = Song(one_song_data)
            song_instances.append(s)
            print(s)
        else:
            one_song_data = {'trackName':"No Results", "artistName":"No Results", "trackTimeMillis": 0}
            s = Song(one_song_data)
            song_instances.append(s)
            print(s)
    except:
        print("There was an error with the iTunes API search for search term:" + tweet.get_longest_word())
        one_song_data = {'trackName':"Error", "artistName":"Error", "trackTimeMillis": 0}
        s = Song(one_song_data)
        song_instances.append(s)
        print(s)

#Creating a list of tuples using the list of Tweet instances and the list of Song instances

tuple_list = list(zip(sorted_tweets, song_instances))

#Writing a CSV file with the following columns, where each row represents 1 tweet and its corresponding song (include headers)
#Tweet Text, Tweet Username, Number Tweet Hashtags, Longest Word in Tweet, Song Name, Song Artist Name, Seconds In Song (not milliseconds)

csv = open("finalproject.csv", "w")
row1 = "Tweet Text, Tweet Username, Number Tweet Hashtags, Longest Word in Tweet, Song Name, Song Artist Name, Song In Seconds" + '\n'
csv.write(row1)
for tup in tuple_list:
    tweet_text = tup[0].text
    tweet_text2 = tweet_text.replace(","," ")
    tweet_text3 = tweet_text2.replace('\n','')
    tweet_username = tup[0].username
    num_tweet_hashtags = tup[0].get_number_hashtags()
    longest_word_in_tweet = tup[0].get_longest_word()
    song_name = tup[1].name
    song_name = song_name.replace(","," ")
    song_artist_name = tup[1].artist_name
    song_artist_name = song_artist_name.replace(","," ")
    seconds_in_song = tup[1].get_song_length_sec()
    row = tweet_text3 + "," + tweet_username + "," + str(num_tweet_hashtags) + "," + longest_word_in_tweet + "," + song_name + "," + song_artist_name + "," + str(seconds_in_song) + '\n'
    csv.write(row)
csv.close()

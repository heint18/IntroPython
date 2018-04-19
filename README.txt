SI 506 W18 FINAL PROJECT README (Project Option 1) 
Author: Tyler Hein

* In ~2-3 sentences, what does your project do?

If you fill out twitter_credentials.py Twitter information and run the program SI506W18_finalproject.py, the program will ask you to input either keyword(s) or a Twitter username. Then, it will find the longest word from 50 tweets found by using the keyword(s) or Twitter username you entered, create a playlist based on those words, and then save information about each tweet and its associated song in a .csv file. 

* What files (by name) are included in your submission? List them all! MAKE SURE YOU INCLUDE EVERY SINGLE FILE YOUR PROGRAM NEEDS TO RUN, as well as a sample version of its output file. (Also make sure your sample output file has a DIFFERENT name than the actual thing your program generates, so we don't overwrite the sample by running your program!)

SI506W18_finalproject.py 
SI506W18finalproject_cache.json
twitter_credentials.py
README.txt
sample_output_finalproject.csv (an example of the output file) 
Final_1.png - Final_4.png (screen shots of the program running in the command window) 

* What Python modules must be pip installed in order to run your submission? List them ALL (e.g. including requests, requests_oauthlib... anything someone running it will need!). Note that your project must run in Python 3.

requests
requests_oauthlib
webbrowser
json
string
twitter_credentials


* Explain SPECIFICALLY how to run your code. We should very easily know, after reading this:

-Open "twitter_credentials.py" in a code editor, populate the fields with your Twitter keys, and save the file. Briefly, in order to get your own Twitter keys, log in to your Twitter account, create an application, and click the "Keys and Access Tokens" tab. There is a link to more documentation within "twitter_credentials.py". 
-Run the file "SI506W18_finalproject.py"
-If this is the first time you have run the code (or the first time in a while), you will be prompted to enter a verifier. The verifier code will appear in an internet browser after you indicate acceptance for the application you created in the first step to access your data.
-There will be a prompt asking whether you would like to search Twitter by a keyword(s) or by a (public) Twitter username. If you don't make a valid selection (e.g., "t", the program will run as if you selected the keyword "mountains" to demonstrate how the program works. If you do make a valid selection, you will be prompted to enter the keyword(s) or username. 
-The program will then go on to do several things, including:
	-Using the keyword(s) or username to access 50 posts from Twitter.
	-Determining the longest word in each of the Twitter posts (note: in some cases, such as when a tweet consists entirely of emojis, the longest word may be a blank). 
	-Printing a sentence about each Tweet using the __str__ method of the class Tweet (note: this means there will be a lot of output in the command window). 
	-Using the longest word in each Twitter post as the search term for data from the iTunes API.
	-Printing a sentence about each song instance using the __str__ method of the class Song (note: the means there will be a lot of output in the command window). 
	-Saving information from each Twitter post and its respective iTunes data in a .csv file ("finalproject.csv")
-You may encounter one of two problems when the program searches the iTunes API:
(1) The longest word from an individual Twitter post as the keyword produces 0 results. In this case, the information about the iTunes data for that Twitter post would be: Song Name: None, Song Artist Name: None, Song In Seconds: 0. 
(2) There may be a problem with the iTunes API search due to an intermittent json error. In this case, a message indicating an error will be printed in the command window. The information about the iTunes data for that Twitter post would be: Song Name: Error, Song Artist Name: Error, Song In Seconds: 0. 

* Where can we find all of the project technical requirements in your code? Fill in with the requirements list below.

REQUIREMENTS LIST:
* Get and cache data from 2 REST APIs (list the lines where the functions to get & cache data begin and where they are invoked):

function to get and cache Twitter data: begins line 76; invoked lines 209,216,222 
function to get and cache iTunes data: begins line 113; invoked line 243

* Define at least 2 classes, each of which fulfill the listed requirements (see requirements sheet):

definition of class Tweet: lines 136-180
definition of class Song: lines 185-197 

* Create at least 1 instance of each class:

creation of instances of class Tweet: lines 211,218,224
creation of instances of class Song: lines 246,251,257

* Invoke the methods of the classes on class instances:

Invoking Tweet __str__ method on Tweet instances: line 232

Invoking Tweet get_number_hashtags methods on Tweet instances: lines 180,229,276

Invoking Tweet get_longest_word method on Tweet instances: lines 180,243,255,277

Invoking Song __str__ method on Song instances: lines 248,253,259

Invoking Song get_song_length_sec method on Song instances: lines 197,282

* At least one sort with a key parameter:

sorting Tweet instances with a key parameter: line 229 

* Define at least 2 functions outside a class (list the lines where function definitions begin):

definition of function to get Twitter tokens: begins line 32
definition of function to create a unique identifier for each Twitter search: begins line 67
definition of function to create a unique identifier for each iTunes search: begins line 105

* Invocations of functions you define:

invoking function to get Twitter tokens: line 58
invoking function to create unique identifier for each Twitter search: line 86
invoking function to create unique identifier for each iTunes search: line 118

* Create a readable file:

writing a .csv file with necessary information: lines 268-285

END REQUIREMENTS LIST

* Put any citations you need below. If you borrowed code from a 506 problem set directly, or from the textbook directly, note that. If you borrowed code from a friend/classmate or worked in depth with a friend/classmate, note that. If you borrowed code from someone else's examples on a website, note that.

I borrowed code from:

In-class twitter example (twitter_example.py and twitter_info.py)
Problem Set 10
In-class programmer example (programmer_class_with_solutions.py) 
Piazza post in response to post titled "Project Option 1: Tweet Text"
In-class twitter pagination example (sample_twitter_paging.py)

* Explain in a couple sentences what should happen as a RESULT of your code running: what CSV or text file will it create? What information does it contain? What should we expect from it in terms of approximately how many lines, how many columns, which headers...?

As a result of the code running, you should expect a .csv file to be created ("finalproject.csv"). It should contain information about each Twitter post and its respective iTunes data. Specifically, there should be 7 columns, the the following headers: Tweet Text, Tweet Username, Number Tweet Hashtags, Longest word in Tweet, Song Name, Song Artist Name, Song In Seconds. There should be 51 rows (1 row for the header and 50 for each Twitter post). 

* Is there anything else we need to know or that you want us to know about your project? Include that here!

I know there is some profanity in some of the tweets that showed up in my search - I apologize for this! It is what showed up in my Twitter search! 

import random
import string
import json
import urllib2

def get_three_rand_characters():
	characters = ""
	for i in range(3):
		choice = random.randrange(0,2)
		if choice == 0:
			characters = characters + random.choice(string.ascii_lowercase)
		else:
			characters = characters + str(random.randrange(1,10))
	return characters

def get_random_login():
	values = {"status":{"code":0,"name":"OK"},"completions":[]}
	while len(values["completions"]) == 0 :
		url = "https://keybase.io/_/api/1.0/user/autocomplete.json?q="+get_three_rand_characters()
		response = urllib2.urlopen(url)
		data = response.read()
		values = json.loads(data)
	user = random.choice(values["completions"])
	return user["components"]["username"]["val"]
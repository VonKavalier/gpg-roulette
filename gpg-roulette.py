import random
import string
import json
import urllib2
import requests
import operator

def get_three_rand_characters():
	characters = ""
	for i in range(3):
		choice = random.randrange(0,2)
		if choice == 0:
			characters = characters + random.choice(string.ascii_lowercase)
		else:
			characters = characters + str(random.randrange(1,10))
	return characters

def get_json(url_param):
	url = url_param
	response = urllib2.urlopen(url)
	data = response.read()
	values = json.loads(data)
	return values

def get_random_login():
	values = {"status":{"code":0,"name":"OK"},"completions":[]}
	while len(values["completions"]) == 0 :
		values = get_json("https://keybase.io/_/api/1.0/user/autocomplete.json?q="+get_three_rand_characters())
	user = random.choice(values["completions"])
	return user["components"]["username"]["val"]

def get_gpg_key():
	key = requests.get("https://keybase.io/"+get_random_login()+"/pgp_keys.asc") 
	key_file = open("pgp_keys.asc","w")
	while key.status_code != 200:
		key = requests.get("https://keybase.io/"+get_random_login()+"/pgp_keys.asc")
	key_file.write(key.text)
	key_file.close()

get_gpg_key()
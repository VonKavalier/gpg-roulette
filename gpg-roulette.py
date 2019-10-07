import random
import string
import json
import urllib2
import requests
import operator
import gnupg

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
    values = get_json("https://keybase.io/_/api/1.0/user/autocomplete.json?q="+get_three_rand_characters())
    while len(values["completions"]) == 0 :
        values = get_json("https://keybase.io/_/api/1.0/user/autocomplete.json?q="+get_three_rand_characters())
    user = random.choice(values["completions"])
    return user["components"]["username"]["val"]

def get_gpg_key():
    key = requests.get("https://keybase.io/"+get_random_login()+"/pgp_keys.asc") 
    #key_file = open("pgp_keys.asc","w")
    while key.status_code != 200:
        key = requests.get("https://keybase.io/"+get_random_login()+"/pgp_keys.asc")
    #key_file.write(key.text)
    #key_file.close()
    return key.text

gpg_home = "~/.gnupg"

gpg = gnupg.GPG(gnupghome=gpg_home)

import_result = gpg.import_keys(get_gpg_key())

savefile = "message.asc"

afile = open("message.txt", "rb")
encrypted_ascii_data = gpg.encrypt_file(afile, import_result.fingerprints, always_trust=True, output=savefile)
afile.close()
str(gpg.delete_keys(import_result.fingerprints[0]))

encrypted_file = open("message.asc","r")
print encrypted_file.read()
encrypted_file.close()

"""
This code attempts to answer the question: how many valid, unique nHentai keys
are there in Pi?

Suprise, suprise. It depends on the length of Pi you feed in. Eventually, you
will get all of nHentai's catalogue.... We're sorry.

Author: Mjr_Mojo
Date: 2020-05-11

Results as of 2020-05-11 @ 20:23 GMT+13:
 - In 1000 digits of Pi there are 327 unique, valid nHentai codes.
 - In 10,000 digits of Pi there are 3092 unique valid nHentai codes. 239 of
   which are in English.
"""

import requests
import json

API_URL_NHENTAI = 'https://nhentai.net/api/gallery/'
REMOVED = "removed"

OUTPUT_FORMAT_STRING = """

============{:^6}============
Title: {}
Language: {}
Tags: {}
==============================
"""

CURRENT_HIGHEST_KEY = 312909 #As of 2020-05-12 @ 16:08 (GMT+12)

pi1000 = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989"

#PI = pi1000

file = open("PI100KDP.TXT")
PI = "3" + file.readline()
file.close()



def get_data_on_this_filth(key):
    request = requests.get(API_URL_NHENTAI + str(key))
    if not request.ok:
        #if the filth has been removed
        return REMOVED, REMOVED, [REMOVED]

    key_data = request.json();
    title_dict = key_data["title"]
    tag_array = key_data["tags"]

    title = title_dict.get("english")
    if title is None:
        #English title doesn't exist
        title = title_dict.get("japanese")

    tags = []
    language = ""
    for tag in tag_array:
        if tag["type"] == 'tag':
            tags.append(tag['name'])
        elif tag["type"] == "language":
            language = tag['name']

    return title, language, tags


sources = []
keys = set()
for i in range(len(PI)-5):
    key = int(PI[i:i+6])
    if key <= CURRENT_HIGHEST_KEY:
        if not key in keys:
            keys.add(key)
            title, language, tags = get_data_on_this_filth(key)
            if title != REMOVED:
                print("{} [{}, {}]: {}".format(title, key, language, tags))
                sources.append([key, title, language, tags])

print("\n\n\n\n\nThere are {} weeb numbers in the first {} digits of Pi".format(len(sources), len(PI)))

eng_sources = [i for i in sources if i[2] == "english"]

print ("{} of them are in english to boot.".format(len(eng_sources)))

output_file = open("output.txt", "w", encoding='utf-8')
for source in sources:
    output_file.write(OUTPUT_FORMAT_STRING.format(source[0], source[1],
                                                  source[2], source[3]))
output_file.close()

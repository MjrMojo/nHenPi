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
import time
import re as ree

API_URL_NHENTAI = 'https://nhentai.net/api/gallery/'
REMOVED = "removed"

OUTPUT_FORMAT_STRING = """

============{:^6}============
Title: {}
Language: {}
Tags: {}
==============================
"""

OUTPUT_HEADER_FORMAT = """There are {num} nHentai doujins in the first {pi_len} digits of \u03C0 as of {timestamp}
Language split: - {lang1_str:13}: {lang1_num:6} ({lang1_perc:>5.2f} %)
                - {lang2_str:13}: {lang2_num:6} ({lang2_perc:>5.2f} %)
                - {lang3_str:13}: {lang3_num:6} ({lang3_perc:>5.2f} %)
                - Uncategorised: {uncat_num:6} ({uncat_perc:>5.2f} %)
"""

VISUALISER_OUTPUT = """{{'title': '{}', 'media_id': '{}',
 'tags': {}, 'location': [{}, {}],
 'language': '{}', 'key': {}}},\n"""

pi1000 = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989"

#PI = pi1000

file = open("PI100KDP.TXT")
PI = "3" + file.readline()
file.close()

title_extract_regex = ree.compile(r'\([^()]*\)|\[[^[]*\]|\{[^{]*\}')

def count(l, key):
    return sum(map(lambda x: x[2] == key, l))


def get_latest_id():
    request = requests.get(API_URL_NHENTAI + "all")
    if not request.ok:
        return 312909, "2020-05-12 @ 16:08 (GMT+1200)"
    else:
        first_result = request.json()["result"][0]
        return int(first_result["id"]), time.strftime("%Y-%m-%d @ %H:%M (GMT%z)")


def get_data_on_this_filth(key):
    request = requests.get(API_URL_NHENTAI + str(key))
    if not request.ok:
        #if the filth has been removed
        return REMOVED, REMOVED, [REMOVED]

    key_data = request.json();
    title_dict = key_data["title"]
    tag_array = key_data["tags"]
    media_key = key_data["media_id"]

    title = title_dict.get("english")
    if title is None:
        #English title doesn't exist
        title = title_dict.get("japanese")

    title = ree.escape(title_extract_regex.sub("", title).strip())

    tags = []
    language = ""
    for tag in tag_array:
        if tag["type"] == 'tag':
            tags.append(tag['name'])
        elif tag["type"] == "language":
            language = tag['name']

    return title, language, tags, media_key


latest_key, latest_key_time_stamp = get_latest_id();

sources = []
keys = set() #the set of already found keys to prevent multiple request
key_occurrence_count = dict()
for i in range(len(PI)-5):
    key = int(PI[i:i+6])
    if key <= latest_key:
        key_occurrence_count[key] = key_occurrence_count.get(key, 0) + 1
        if not key in keys: #ensure the key is unique to prevent duplicates
            keys.add(key)
            title, language, tags, media_key = get_data_on_this_filth(key)
            if title != REMOVED:
                print("{} [{}, {}]: {}".format(title, key, language, tags))
                sources.append([key, title, language, tags, media_key, (i, i + 6)])

print("\n\n\n\n\nThere are {} weeb numbers in the first {} digits of Pi".format(len(sources), len(PI)))

print ("{} of them are in english to boot.".format(count(sources, "english")))

output_file = open("output.txt", "w", encoding='utf-8')

#Count the number of sources we have.
num = len(sources)
num_eng = count(sources, "english")
num_jap = count(sources, "japanese")
num_chin = count(sources, "chinese")
num_uncat = num - (num_eng + num_jap + num_chin)

#Create the lang_num array and order it based on which language is the most to
#least prevalent. This is the order in which they will be displayed in the
#output header.
lang_num = [(num_eng, "english"), (num_jap, "japanese"), (num_chin, "chinese")]
lang_num.sort(key=lambda x: x[0], reverse=True)

output_file.write(OUTPUT_HEADER_FORMAT.format(num=num,
                                              pi_len=len(PI) - 1,
                                              timestamp=latest_key_time_stamp,
                                              lang1_str=lang_num[0][1].title(),
                                              lang2_str=lang_num[1][1].title(),
                                              lang3_str=lang_num[2][1].title(),
                                              lang1_num=lang_num[0][0],
                                              lang2_num=lang_num[1][0],
                                              lang3_num=lang_num[2][0],
                                              uncat_num=num_uncat,
                                              lang1_perc=(lang_num[0][0] / num) * 100,
                                              lang2_perc=(lang_num[1][0] / num) * 100,
                                              lang3_perc=(lang_num[2][0] / num) * 100,
                                              uncat_perc=(num_uncat / num) * 100))

for source in sources:
    output_file.write(OUTPUT_FORMAT_STRING.format(source[0], source[1],
                                                  source[2], source[3]))
output_file.close()


output_file = open("visualiser_dataset.js", "w", encoding='utf-8')

output_file.write("dataset = [\n")
for source in sources:
    output_file.write(VISUALISER_OUTPUT.format(source[1], source[4],
                                               source[3], source[5][0],
                                               source[5][1], source[2],
                                               source[0]))
output_file.write("]")
output_file.close()

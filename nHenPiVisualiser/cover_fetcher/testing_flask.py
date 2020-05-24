from flask import Flask
from flask_cors import CORS
import requests
import subprocess
import time

NHENTAI_COVER_GALLERY = "https://t.nhentai.net/galleries/{}/cover.{}"

app = Flask(__name__)

CORS(app)

if __name__ == '__main__':
    app.run(threaded=True)

@app.route('/')
def hello_world():
    return "Hello, World!"

def calc_time(start, end):
    return (end - start) * 1000

@app.route("/fetch_cover/<media_key>")
def get_cover_from_nhentai(media_key):
    start_time = time.time()
    url = NHENTAI_COVER_GALLERY.format(media_key, "jpg")
    request = requests.get(url, stream = True)
    if not request.ok:
        #if the request fails try to get the .png version
        url = NHENTAI_COVER_GALLERY.format(media_key, "png")
        request = requests.get(url, stream = True)
        if not request.ok:
            #we couldn't even get the png version, just give up
            print("Handling request took {:.2f}".format(time.time() - start_time))
            return "done"

    #if we managed to retrieve one of the versions save it out
    #if its a png store it as a jpg any way
    filename = "{}.jpg".format(media_key)
    request.raw.decode_content = True
    with open(filename, 'wb') as f:
        for section in request:
            f.write(section)
    subprocess.call(["./pixelate.sh", filename, filename])
    print("Handling request took {:.2f}".format(time.time() - start_time))
    return "done"

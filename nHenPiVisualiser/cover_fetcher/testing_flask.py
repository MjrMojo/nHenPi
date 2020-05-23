from flask import Flask
from flask_cors import CORS
import requests
import subprocess
import time

NHENTAI_COVER_GALLERY = "https://t.nhentai.net/galleries/{}/cover.{}"

app = Flask(__name__)

CORS(app)

LOG = "Request.get: {:.3f} ms\nWriting Cover: {:.3f} ms\nPixelation: {:.3f} ms"

if __name__ == '__main__':
    app.run(threaded=True)

@app.route('/')
def hello_world():
    return "Hello, World!"

def calc_time(start, end):
    return (end - start) * 1000

@app.route("/fetch_cover/<media_key>")
def get_cover_from_nhentai(media_key):
    url = NHENTAI_COVER_GALLERY.format(media_key, "jpg")
    req_start_time = time.time()
    request = requests.get(url, stream = True)
    req_end_time = time.time()

    if request.ok:
        filename = "{}.jpg".format(media_key)
        request.raw.decode_content = True
        with open(filename, 'wb') as f:
            for section in request:
                f.write(section)
        file_write_end_time = time.time()
        subprocess.call(["./pixelate.sh", filename, filename])
        pixelate_end_time = time.time()
        print(LOG.format(calc_time(req_start_time, req_end_time),
                         calc_time(req_end_time, file_write_end_time),
                         calc_time(file_write_end_time, pixelate_end_time)))
        return "done"
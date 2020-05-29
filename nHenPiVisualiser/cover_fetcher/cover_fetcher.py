from flask import Flask
#from flask_cors import CORS
from flask_api import status
import requests
import subprocess
import time
import threading

NHENTAI_COVER_GALLERY = "https://t.nhentai.net/galleries/{}/cover.{}"

app = Flask(__name__)

#CORS(app)


currently_processing = dict() #dict of semaphores with key of the media ID
num_waiting = dict() #dict of the number of waiting threads for a given media ID (the key)
currently_processing_lock = threading.Lock()

if __name__ == '__main__':
    app.run(threaded=True)

@app.route('/')
def hello_world():
    return "Hello, World!"

def calc_time(start, end):
    return (end - start) * 1000


def get_cover(media_key):
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
    filename = "/var/www/nhenpi.net/covers/{}.jpg".format(media_key)
    request.raw.decode_content = True
    with open(filename, 'wb') as f:
        for section in request:
            f.write(section)
    subprocess.call(["./pixelate.sh", filename, filename])
    subprocess.call(["mv", filename, filename]) #f"/var/www/nhenpi.net/covers/{filename}"])
    print("Handling request took {:.2f}".format(time.time() - start_time))
    return "done"


@app.route("/fetch_cover/<int:media_key>")
def get_cover_from_nhentai(media_key):
    currently_processing_lock.acquire(timeout=5)
    if currently_processing_lock.locked():
        #we have got the lock
        if num_waiting.get(media_key, None) is None:
            #No one else has asked for this cover yet
            currently_processing[media_key] = threading.Semaphore(value=0)
            num_waiting[media_key] = 1;
            currently_processing_lock.release()

            get_cover(media_key) #do the job

            #once we have retrieved the cover release waiting threads. NB: we
            #will wait for as long as necessary to release the child threads.
            currently_processing_lock.acquire()
            for i in range(num_waiting[media_key]):
                currently_processing[media_key].release()
            num_waiting.pop(media_key)
            currently_processing_lock.release()
            return "done"

        else:
            #we aren't the first one to ask for this, so we must wait our turn.
            #First notify the other thread that we're waiting on its result,
            #before releasing the lock and waiting for the result.
            num_waiting[media_key] += 1;
            temp = currently_processing[media_key]
            currently_processing_lock.release()

            #Wait for the thread which is doing the process to release you
            #before returning done to the client
            if temp.acquire(timeout=5):
                return "done"
            else:
                #we've waited too long, just return an error
                return "", status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        #attempt to acquire lock timed out, return an error
        return "", status.HTTP_503_SERVICE_UNAVAILABLE

import threading
import http.client
import json
import sys

class CouchDbVersionThread(threading.Thread):
    def __init__(self, wfile):
        threading.Thread.__init__(self)
        self.wfile = wfile

    def run(self):
        http_connection = http.client.HTTPConnection("localhost", 5984)
        http_connection.request("GET", "/")
        http_response = http_connection.getresponse()
        http_body = http_response.read()
        json_string = http_body.decode("UTF-8")
        self.jsonObject = json.loads(json_string)
        try :
            self.wfile.write(bytes(json.dumps(self.jsonObject), "UTF-8"))
        except TypeError:
            self.wfile.write(json.dumps(self.jsonObject))

    def getCouchDbVersion(self):
        return self.jsonObject


if __name__ == "__main__":
    couch_db_version_thread = CouchDbVersionThread(sys.stderr)
    couch_db_version_thread.start()
    couch_db_version_thread.join()
    dir(couch_db_version_thread.getCouchDbVersion())
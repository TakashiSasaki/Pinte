import threading
import http.client
import json
import sys

class CouchbaseVersionThread(threading.Thread):
    def __init__(self, wfile):
        threading.Thread.__init__(self)
        self.wfile = wfile

    def run(self):
        http_connection = http.client.HTTPConnection("localhost", 8092)
        http_connection.request("GET", "/")
        http_response = http_connection.getresponse()
        http_body = http_response.read()
        json_string = http_body.decode("UTF-8")
        self.jsonObject = json.loads(json_string)
        try :
            self.wfile.write(bytes(json.dumps(self.jsonObject), "UTF-8"))
        except TypeError:
            self.wfile.write(json.dumps(self.jsonObject))

    def getCouchbaseVersion(self):
        return self.jsonObject


if __name__ == "__main__":
    couchbase_version_thread = CouchbaseVersionThread(sys.stderr)
    couchbase_version_thread.start()
    couchbase_version_thread.join()
    dir(couchbase_version_thread.getCouchbaseVersion())

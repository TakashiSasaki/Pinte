import threading
import http.client
import json
import sys

class ArangoDbVersionThread(threading.Thread):
    def __init__(self, wfile):
        threading.Thread.__init__(self)
        self.wfile = wfile

    def run(self):
        http_connection = http.client.HTTPConnection("localhost", 8529)
        http_connection.request("GET", "/_api/version")
        http_response = http_connection.getresponse()
        http_body = http_response.read()
        json_string = http_body.decode("UTF-8")
        self.jsonObject = json.loads(json_string)
        try :
            self.wfile.write(bytes(json.dumps(self.jsonObject), "UTF-8"))
        except TypeError:
            self.wfile.write(json.dumps(self.jsonObject))

    def getArangoDbVersion(self):
        return self.jsonObject


if __name__ == "__main__":
    arango_db_version_thread = ArangoDbVersionThread(sys.stderr)
    arango_db_version_thread.start()
    arango_db_version_thread.join()
    dir(arango_db_version_thread.getArangoDbVersion())

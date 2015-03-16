#!/usr/bin/python3
import http.server
import http.cookies
import http.cookiejar
import time
import sys
import logging
logging.basicConfig(level=logging.INFO)

SERVER_ADDRESS = "127.1.2.3"
SERVER_PORT = 13579

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        logging.getLogger().info("do_GET\n")
        logging.getLogger().info(self.headers)

        simple_cookie_in_request = http.cookies.SimpleCookie()
        logging.getLogger().info("self.headers = " + str(self.headers))
        try:
            simple_cookie_in_request.load(self.headers["Cookie"])
        except AttributeError as e:
            logging.getLogger("no Cookie header in request")
        logging.getLogger().info("simple_cookie_in_request")
        logging.getLogger().info(simple_cookie_in_request)

        saveSimpleCookie(simple_cookie_in_request)
        loadSimpleCookie()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        simple_cookie_in_response = http.cookies.SimpleCookie()
        simple_cookie_in_response["responded_time"] = time.asctime()
        simple_cookie_in_response["hello"] = "world"

        logging.getLogger().info("simple_cookie_in_response")
        logging.getLogger().info(simple_cookie_in_response)
        for x in simple_cookie_in_response:
            self.send_header("Set-Cookie", simple_cookie_in_response[x].OutputString())
        self.end_headers()

        self.wfile.write(bytes("Hello at " + time.asctime() + "\r\n", "UTF-8"))

def saveSimpleCookie(simple_cookie):
    f = open("simple_cookie.txt", "w")
    f.write(simple_cookie.output())
    f.close()

def loadSimpleCookie():
    f = open("simple_cookie.txt", "r")
    simple_cookie = http.cookies.SimpleCookie()
    simple_cookie.load(f.read())
    logging.getLogger().info("loadSimpleCookie")
    logging.getLogger().info(simple_cookie)

if __name__ == "__main__":
    http_server = http.server.HTTPServer((SERVER_ADDRESS, SERVER_PORT), MyRequestHandler)
    while True:
        logging.getLogger().info("handle_request at " + time.asctime())
        http_server.handle_request()

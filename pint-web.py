#!/usr/bin/python3
import http.server
import http.cookies
import http.cookiejar
import time
import sys
import logging


SERVER_ADDRESS = ""
SERVER_PORT = 13579


class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("do_GET\n")
        print(self.headers)

        simple_cookie_in_request = http.cookies.SimpleCookie()
        simple_cookie_in_request.load(self.headers["Cookie"])
        print("simple_cookie_in_request")
        print(simple_cookie_in_request)

        saveSimpleCookie(simple_cookie_in_request)
        loadSimpleCookie()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        simple_cookie_in_response = http.cookies.SimpleCookie()
        simple_cookie_in_response["responded_time"] = time.asctime()
        simple_cookie_in_response["hello"] = "world"

        print("simple_cookie_in_response")
        print(simple_cookie_in_response)
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
    print("loadSimpleCookie")
    print(simple_cookie)

if __name__ == "__main__":
    http_server = http.server.HTTPServer((SERVER_ADDRESS, SERVER_PORT), MyRequestHandler)
    while True:
        print("handle_request at " + time.asctime(), file=sys.stderr)
        http_server.handle_request()

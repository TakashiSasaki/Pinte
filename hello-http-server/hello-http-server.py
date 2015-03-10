#!/usr/bin/python3
import http.server, http.cookies

SERVER_ADDRESS = ""
SERVER_PORT = 13579


def main():
    http_server = http.server.HTTPServer((SERVER_ADDRESS, SERVER_PORT), MyRequestHandler)
    http_server.handle_request()
   
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.wfile.write(bytes("Hello.\r\n", "UTF-8"))
        if "cookie" in self.headers:
            self.cookie=http.cookies.SimpleCookie(self.headers.getheader("cookie"))
            for x in self.cookie:
                self.wfile.write(bytes(x + "\r\n", "UTF-8"))

if __name__ == "__main__":
    main()

import os
import socketserver
import http.server

#dir_esecuzione = os.path.join(os.path.dirname(__file__), 'server')
#os.chdir(dir_esecuzione)

def run():
    PORT = 8000

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()
#hexkey = keys.AESkey.hex()
#bytekey = bytes.fromhex(hexkey)
#curl localhost:8008/   -H "Content-Type: application/json"   -X POST --data '{"keyAES":"91", "keyPubRSA":"92", "keyPrivRSA":"94"}

from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv
import json
import Database.sqlite as bbdd

BIND_HOST = 'localhost'
PORT = 8008


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.write_response(b'')

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)

        self.write_response(body)

    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        #self.wfile.write(content)

        content = content.decode('utf-8')        
        json_content = json.loads(content)
        data = (bytes.fromhex(json_content["keyAES"]), bytes.fromhex(json_content["keyPubRSA"]), bytes.fromhex(json_content["keyPrivRSA"]), '0')
        bbdd.sql_insert(data)

if len(argv) > 1:
    arg = argv[1].split(':')
    BIND_HOST = arg[0]
    PORT = int(arg[1])

print(f'Listening on http://{BIND_HOST}:{PORT}\n')

httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()

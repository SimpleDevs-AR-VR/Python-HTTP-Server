from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import json

import time

_HOST = "10.18.171.66"
_PORT = 9999

class NeuralHTTP(BaseHTTPRequestHandler):
    # Handles GET requests. Defaults to a simple HELLO WORLD webpage
    def do_GET(self):
        # Send response code (success)
        self.send_response(200)
        # Define header of response
        self.send_header("Content-type","text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>HELLO WORLD!</h1></body></html>", "utf-8"))
    
    # Handles POST requests. It only requests JSON content
    def do_POST(self):
        # Detect the ctype and pdict of the request
        ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))

        # We refuse if the content type is not json
        if ctype != 'application/json':
            self.send_response(400, "Method not allowed")
            self.end_headers()
            self.wfile.write("POST only accepts application/json content\n".encode())
            return

        # Read the message
        length = int(self.headers.get('Content-length'))
        payload_string = self.rfile.read(length).decode('utf-8')
        payload = json.loads(payload_string) if payload_string else None
        print(payload)

        # Send response code (success)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"recieved":true}',"utf-8"))

# To host this server, execute the following command in your bash terminal, 
#   in the directory of your choice:
# python -m http.server <_PORT> --bind <_HOST>
# python -m http.server <_PORT> -b <_HOST>

# To test these, follow these commands inside your bash terminal
# - Testing GET: curl <_HOST>:<_PORT> -X GET
# - Testing POST: curl <_HOST>:<_PORT> _X POST
# Or get an app like Postman to test more robustly

server = HTTPServer(
    (_HOST, _PORT),
    NeuralHTTP
)
print("Server now running on {}:{}".format(_HOST, _PORT))

server.serve_forever()
server.server_close()
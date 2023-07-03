from http.server import HTTPServer, BaseHTTPRequestHandler
import time

_HOST = "10.11.43.12"
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
    
    # Handles POST requests. For now, it just merely sends back the time in JSON
    def do_POST(self):
        # Send response code (success)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes('{"time":"' + date + '"}',"utf-8"))

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
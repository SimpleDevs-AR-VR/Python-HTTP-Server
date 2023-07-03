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

server = HTTPServer(
    (_HOST, _PORT),
    NeuralHTTP
)
print("Server now running on {}:{}".format(_HOST, _PORT))

server.serve_forever()
server.server_close()
import json
import threading

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/terminate"):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write("Server shutting down...".encode())

            threading.Thread(target=self.shutdown_server).start()
        else:
            print('Request path is:', self.path)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response_data = {
                "example key": "example value",
                "example int key": 123
            }
            response_data_json = json.dumps(response_data)
            self.wfile.write(response_data_json.encode())

    def shutdown_server(self):
        self.server.shutdown()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('127.0.0.1', 8000)
    print('starts on:', server_address[0] + ':' + str(server_address[1]))
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == '__main__':
    run(handler_class=HttpHandler)

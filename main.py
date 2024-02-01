import json

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('new request!')
        print('path is:', self.path)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # TODO: routing
        response_data = {"key": "value", "int key": 123}
        response_data_json = json.dumps(response_data)
        self.wfile.write(response_data_json.encode())


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
    except ...:
        print("Server stopped with unhandled error!")


if __name__ == '__main__':
    run(handler_class=HttpHandler)

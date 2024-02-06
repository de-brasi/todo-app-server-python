import json
import threading

from typing import Dict

from urllib.parse import urlparse
from urllib.parse import parse_qs

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


class HttpHandler(BaseHTTPRequestHandler):
    @staticmethod
    def parse_querystring_args(url: str) -> Dict:
        parse_result = urlparse(url)
        dict_result = parse_qs(parse_result.query)
        return dict_result

    @staticmethod
    def parse_query_params(url: str):
        parse_result = urlparse(url)
        result = parse_result.params
        return result

    @staticmethod
    def parse_path(url) -> str:
        return urlparse(url).path

    def set_main_headers(self, content_type: str, access_control: str) -> None:
        self.send_header("Content-type", content_type)
        self.send_header(
            "Access-Control-Allow-Origin", access_control
        )
        self.end_headers()

    def set_response(self, response_code: int, content_type: str, access_control: str, message: str) -> None:
        self.send_response(response_code)
        self.set_main_headers(content_type, access_control)
        self.wfile.write(message.encode())

    def do_GET(self):
        if self.path.startswith("/get-tasks"):
            print('Request path is:', self.path)

            response_data = {
                "example key": "example value",
                "example int key": 123
            }
            response_data_json = json.dumps(response_data)
            self.set_response(200,
                              "application/json",
                              "*",
                              response_data_json)

        else:
            self.set_response(404,
                              "text/plain",
                              "*",
                              "Not expected endpoint")

    def do_POST(self):
        requested_url = self.path
        requested_endpoint = HttpHandler.parse_path(requested_url)
        request_querystring_args = HttpHandler.parse_querystring_args(requested_url)
        request_body_args = HttpHandler.parse_query_params(requested_url)

        if requested_endpoint.startswith('/add-task'):
            response_data = {
                "test POST request status": "handled",
                "got data": request_querystring_args
            }
            response_data_json = json.dumps(response_data)

            self.set_response(200,
                              "application/json",
                              "*",
                              response_data_json)

        elif requested_endpoint.startswith('/add-task') or requested_endpoint.startswith('/shutdown'):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write("Server shutting down...".encode())

            threading.Thread(target=self.shutdown_server).start()
        else:
            self.set_response(404,
                              "text/plain",
                              "*",
                              "Not expected endpoint")

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

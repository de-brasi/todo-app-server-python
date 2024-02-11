import threading

from typing import Dict

from urllib.parse import urlparse
from urllib.parse import parse_qs

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from core.services import MainService
from infrastructure.db.repositories import TasksRepositoryCSV


class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.main_service = MainService(TasksRepositoryCSV())
        super().__init__(request, client_address, server)

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

            response_data_json = self.main_service.get_tasks_from_db()
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

        # todo: debug only
        print("url:", requested_url)
        print("endpoint:", requested_endpoint)
        print("querystring args:", request_querystring_args)
        print("body args:", request_body_args)

        if requested_endpoint.startswith('/add-task'):
            # todo: надо ли что-то отвечать на это?
            # todo: надо распарсить нужные поля согласно

            # TODO:
            #  написать документирующий комментарий,
            #  что ожидаются запросы в формате ..url../?tasks=[<json string:>{},{},{}]

            querystring_field_name_for_tasks = 'tasks'
            tasks_index = 0

            try:
                print(
                    f"Got query string with python type"
                    f"{type(request_querystring_args[querystring_field_name_for_tasks][tasks_index])}:",
                    request_querystring_args[querystring_field_name_for_tasks][tasks_index]
                )

                self.main_service.save_tasks_to_db(
                    request_querystring_args[querystring_field_name_for_tasks][tasks_index])

                self.set_response(200,
                                  "text/plain",
                                  "*",
                                  "Saved success")
            except ...:
                self.set_response(500,
                                  "text/plain",
                                  "*",
                                  "Error occurred when handling request")

        elif requested_endpoint.startswith('/terminate') or requested_endpoint.startswith('/shutdown'):
            self.set_response(200,
                              "text/plain",
                              "*",
                              "Server shutting down...")

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

from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import socket
from threading import Thread
import urllib.parse

from utils.my_logger import MyLogger
from utils.base import BASE_DIR, DATA_JSON
from sock_server import run_socket_server

logging = MyLogger("main").get_logger()
SERVER_IP = '127.0.0.1'

SOCKET_PORT = 5000
SERVER_PORT = 3000


def send_data_to_soket(body: bytes):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body, (SERVER_IP, SOCKET_PORT))
    client_socket.close()
    
    
class GoitHttpHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        send_data_to_soket(body)
        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()
        
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/':
                self.send_html_file('index.html')
            case '/message':
                self.send_html_file('message.html')
            case _:
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)
                else:    
                    self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
            
    def send_static(self, filename):
        self.send_response(200)
        mime_tipe, _ = mimetypes.guess_type(filename)
        mime_tipe = mime_tipe if mime_tipe else 'text/plain'
        
        self.send_header('Content-type', mime_tipe)  
        self.end_headers()
        
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())        


def run(server_class=HTTPServer, handler_class=GoitHttpHandler):
    server_address = ('', SERVER_PORT)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
        http.shutdown()




if __name__ == '__main__':
    
    thread_server = Thread(target=run)
    thread_server.start()
    
    thread_socket = Thread(target=run_socket_server, args=(SERVER_IP, SOCKET_PORT))
    thread_socket.start()
    
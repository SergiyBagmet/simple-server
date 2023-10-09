from http.server import HTTPServer, BaseHTTPRequestHandler
import pathlib
import urllib.parse
import mimetypes


BASE_DIR = pathlib.Path()

class HttpHandler(BaseHTTPRequestHandler):
    
    
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/':
                self.send_html_file('index.html')
            case'/message':
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
        mime_tipe, *_ = mimetypes.guess_type(filename)
        mime_tipe = mime_tipe if mime_tipe else 'text/plain'
        
        self.send_header('Content-type', mime_tipe)  
        self.end_headers()
        
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())        


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
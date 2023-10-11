from pathlib import Path
import socket
from datetime import datetime
import urllib.parse
import json

from utils.base import DATA_JSON
from utils.my_logger import MyLogger

logging = MyLogger(name="soket", log_level=10, log_file='parse.log').get_logger()


BUFFER = 1024

def get_data(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as fd:
        return json.load(fd)

def save_data(body: bytes, path: Path):
    data = urllib.parse.unquote_plus(body.decode())
    try:
        payload = {
            str(datetime.now()):{
                k: vl[0].strip() for k, vl in urllib.parse.parse_qs(qs=data, 
                                                                    strict_parsing=True, 
                                                                    keep_blank_values=True,
                                                                    max_num_fields=2
                                                                    ).items()
                }
            }
        if (storage_data:= get_data(path)):
            payload.update(storage_data)
        with open(path, 'w', encoding='utf-8') as fd:
            json.dump(payload, fd, ensure_ascii=False, indent=4)    
    except ValueError as err:
        logging.error(f'Field parse data -- {data} with error: {err}')    
    except OSError as err:
        logging.error(f'Field write dat -- {data} with error: {err}')
        
def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data = server_socket.recv(BUFFER)
            save_data(data, DATA_JSON)
    except KeyboardInterrupt:
        logging.info('Socket server stoped')
    finally:
        server_socket.close()    
        
        
        
if __name__ == '__main__':
    pass
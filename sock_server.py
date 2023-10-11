from pathlib import Path
import socket
from datetime import datetime
import urllib.parse
import json
import typing as t

from utils.const import DATA_JSON, BUFFER
from utils.my_logger import MyLogger

logging = MyLogger(name="soket", log_level=10, log_file='parse.log').get_logger()


class FormDataParser:
    

    def __init__(self, body: bytes) -> None:
        self.body = body
        self.data = urllib.parse.unquote_plus(body.decode())
    
    def _parser(self) -> dict[str, str]:
        try:
            return {
                k: vl[0].strip() for k, vl in urllib.parse.parse_qs(qs=self.data, 
                                                                    strict_parsing=True, 
                                                                    keep_blank_values=True,
                                                                    ).items()
            }
        except ValueError as err:
            logging.error(f'Field parse data -- {self.data} with error: {err}')   
    
    def hash_data(self, hash: t.Hashable) -> dict[t.Hashable, dict[str, str]]:
        return {hash : self._parser()}


class InvalidJsonFileError(Exception):
    pass


class JsonDataHandler:
    
    
    def __init__(self, json_path: Path) -> None:
        self.json_path = json_path
        
    @property
    def json_path(self) -> Path:
        return self._json_path 
    
    @json_path.setter
    def json_path(self, json_path: Path) -> None:
        if not json_path.exists():
            logging.error(f'FileNotFoundError "{json_path}" ')
            raise FileNotFoundError(f'File "{json_path}" not found')
        if json_path.suffix != '.json':
            logging.error(f'InvalidJsonFileError "{json_path}"')
            raise InvalidJsonFileError(f'File "{json_path}" has an invalid extension. It must be a .json file.')
        self._json_path = json_path      
    
    def get_data(self) -> dict:
        try:
            with open(self.json_path, 'r', encoding='utf-8') as fd:
                return json.load(fd) 
        except json.JSONDecodeError as err:
            logging.error(f'JSONDecodeError: {err}') 
          
    def save_data(self, data: dict) -> None:
        if storage_data:= self.get_data():
                data.update(storage_data)
        try:
            with open(self.json_path, 'w', encoding='utf-8') as fd:
                json.dump(data, fd, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as err:
            logging.error(f'JSONDecodeError: {err}')                   
        except OSError as err:
            logging.error(f'Field write dat "{data}" with error: {err}')

   
   
def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data_bytes = server_socket.recv(BUFFER)
            form_data = FormDataParser(data_bytes)
            data = form_data.hash_data(str(datetime.now()))
            jsone_data = JsonDataHandler(DATA_JSON)
            jsone_data.save_data(data)
    except KeyboardInterrupt:
        logging.info('Socket server stopped by user')
    except OSError as err:
        logging.error(f'Socket server error: {err}')
    finally:
        server_socket.close()
        logging.info('Socket server closed')   
                     
if __name__ == '__main__':
    pass
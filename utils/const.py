from enum import Enum, IntEnum, unique
import pathlib

BASE_DIR = pathlib.Path()

DATA_JSON = BASE_DIR.joinpath('storage/data.json')

class Localhost(Enum): 
    SERVER_IP = '127.0.0.1'
    SOCKET_PORT = 5000
    SERVER_PORT = 3000


BUFFER = 1024

@unique
class HttpStatus(IntEnum):
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SEE_OTHER = 303 

if __name__ == '__main__':
    pass
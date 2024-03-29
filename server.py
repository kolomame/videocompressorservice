
import socket
import os
from pathlib import Path


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '0.0.0.0'
server_port = 9001


dpath = 'temp'
if not os.path.exists(dpath):
    os.makedirs(dpath)

print('Starting up on {} port {}'.format(server_address, server_port))

sock.bind((server_address, server_port))
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        header = connection.recv(8)

        filename_length = int.from_bytes(header[:1], "big")
        json_length = int.from_bytes(header[1:3], "big")
        data_length = int.from_bytes(header[4:8], "big")
        stream_rate = 4096

        print('Received header from client. Byte lengths: Title length {}, JSON length {}, Data Length {}'.format(filename_length, json_length,data_length))
        filename = connection.recv(filename_length).decode('utf-8')

        if json_length != 0:
            raise Exception('JSON data is not currently supported.')

        if data_length == 0:
            raise Exception('No data to read from client.')

        with open(os.path.join(dpath, filename),'wb+') as f:
            while data_length > 0:
                data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                f.write(data)
                print('recieved {} bytes'.format(len(data)))
                data_length -= len(data)
                print(data_length)

        print('Finished downloading the file from client.')
    except Exception as e:
        print('Error: ' + str(e))

    finally:
        print("Closing current connection")
        connection.close()
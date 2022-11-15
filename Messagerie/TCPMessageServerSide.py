import socket

host = "192.168.1.20"
port = 9990

#Socket creation
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host,port))
socket.listen(1)
client_socket, address = socket.accept()
print(f'Connection {address[0]}:{address[1]}')


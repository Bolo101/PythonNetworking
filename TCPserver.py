import socket
import threading

ip = "0.0.0.0"
port = 9999

def main():
    server= socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    print("Server listening on {} : {}".format(ip,port))

    while True:
        client_socket,address = server.accept()
        print(f'Entering connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target = handle_client, args=(client_socket))
        client_handler.start()

def handle_client(socket_of_the_client):
    with socket_of_the_client as sock:
        request = sock.recv(1024)
        print(f'Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()

    
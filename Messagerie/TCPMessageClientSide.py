import socket

host = "127.0.0.1"
port = 9990

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

while True:
    flow = input('->')
    client.send(flow.encode('utf-8'))

    server_request = client.recv(400)
    server_request = server_request.decode('utf-8')
    print('Received {}'.format(server_request))





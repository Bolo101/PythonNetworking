import socket
import threading

host = "127.0.0.1"
port = 9990

#define sending and receiving functions
def Receiving(client):
    while True:
        server_request = client.recv(400)
        server_request = server_request.decode('utf-8')
        print('Received {}'.format(server_request))

def Sending(client):
    while True:
        flow = input('->')
        client.send(flow.encode('utf-8'))
        print(f'Sended {flow}')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

#def Thread object
envoie = threading.Thread(target=Sending, args=(client,))
receiv = threading.Thread(target=Receiving,args=(client,))

envoie.start()
receiv.start()

    

    





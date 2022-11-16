import socket 


target_host = "127.0.0.1"
target_port = 9999

#create socket
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to client
client.connect((target_host,target_port))

#send data
client.send(b"Send")

#receive data
response=client.recv(4096)

print(response.decode())
client.close()

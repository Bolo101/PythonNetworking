import socket 


target_host = "www.google.com"
target_port = 80

#create socket
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to client
client.connect((target_host,target_port))

#send data
client.send(b"GET / HTTP/1.1\r\nhost: google.com\r\n\r\n")

#receive data
response=client.recv(4096)

print(response.decode())
client.close()

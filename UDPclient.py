import socket

# define target 
target_host = "127.0.0.1"  
target_port = 6789

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Garbage data",(target_host,target_port))
data, addr = client.recvfrom(4096)  #two output from recvfrom()
print(data.decode())
client.close()

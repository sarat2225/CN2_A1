import socket
import os
from time import time
import timeit

# HOST = socket.gethostbyname(socket.gethostname())
HOST = "192.168.0.116"
PORT = 9999
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

BUFFER_SIZE = 4096
FORMAT = 'utf-8' 

print(f"Client starting in {HOST}...")
print("\n")

while True:

    file_name = input("Enter file Name: ")

    client.sendto(file_name.encode(FORMAT), ADDR)

    data,addr = client.recvfrom(BUFFER_SIZE)
    fn = data.strip()


    packets = 0
    data,addr = client.recvfrom(BUFFER_SIZE)


    if data.decode(FORMAT) == "NO":
        print("File doesn't exist")
        print("\n")
        continue

    data,addr = client.recvfrom(BUFFER_SIZE)

    print ("Receiving File:",fn.decode(FORMAT))
    f = open(fn,'wb')
    start = timeit.default_timer()
    try:
        while(data):
            f.write(data)
            client.settimeout(2)
            packets += 1
            data,addr = client.recvfrom(BUFFER_SIZE)
    except socket.timeout:
        f.close()
        stop = timeit.default_timer()
        time_taken = stop - start - 2
        size = os.path.getsize(file_name)
        print ("File Downloaded")
        print(f"No. of packets received: {packets}")
        print(f"No. of bytes received: {size}")
        print(f"Time Taken: {time_taken} s")
        print(f"Speed: {(size/time_taken)/1024: .2f} kB/s")
        print()
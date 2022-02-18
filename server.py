import socket
import os
from time import time
import timeit

# HOST = socket.gethostbyname(socket.gethostname())
HOST = "192.168.1.204"
PORT = 9999

file_dict = {}

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind((HOST, PORT))

BUFFER_SIZE = 8192
FORMAT = 'utf-8' 

print(f"Server starting in {HOST}...")
print("\n")

while True:

    data,addr = server.recvfrom(BUFFER_SIZE)
    fn = data.strip()

    packets = 0
    
    start = timeit.default_timer()

    data,addr = server.recvfrom(BUFFER_SIZE)
    total_packets = int(data.decode(FORMAT))
    print(total_packets)

    data,addr = server.recvfrom(BUFFER_SIZE)

    print ("Receiving File:",fn.decode(FORMAT))
    f = open(fn,'wb')

    try:
        while(data):
            p_id = int(data[:5])
            data = data[5:]

            file_dict[p_id] = data

            server.sendto(str(p_id).encode(FORMAT), addr)
            server.settimeout(2)
            packets += 1
            data,addr = server.recvfrom(BUFFER_SIZE)
    except socket.timeout:
        stop = timeit.default_timer()
        time_taken = stop - start - 2
        size = os.path.getsize(fn)
        print ("File Downloaded")

        for i in range(len(file_dict.keys())):
            f.write(file_dict[i])
        f.close()

        print(f"No. of packets received: {packets}")
        print(f"No. of bytes received: {size}")
        print(f"Time Taken: {time_taken} s")
        print(f"Speed: {(size/time_taken)/1024: .2f} kB/s")
        print(len(file_dict.keys()))

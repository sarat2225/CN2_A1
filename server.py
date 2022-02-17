import socket
import os
import math
import time

# 10.0.0.253 - server
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
BUFFER_SIZE = 8192
FORMAT = 'utf-8'

packets_dict = {}
ack = []

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"Server starting in {HOST}...")

while True:

    data, addr = server.recvfrom(BUFFER_SIZE)
    print(f"Requested file: {data.decode(FORMAT)}")

    file_name=data.decode(FORMAT)

    server.sendto(file_name.encode(FORMAT),addr)

    if not os.path.exists(file_name):
        print("Requested file doesn't exist")
        string = "NO"
        server.sendto(string.encode(FORMAT), addr)
        continue
    
    string = "YES"
    server.sendto(string.encode(FORMAT), addr)

    file_size = os.path.getsize(file_name)
    total_packets = math.ceil(file_size / 8187)

    for i in range(total_packets):
        ack.append(0)

    string = str(total_packets)
    server.sendto(string.encode(FORMAT), addr)

    f=open(file_name,"rb")
    data = f.read(BUFFER_SIZE - 5)
    p_id = 0
    packets = 0
    while (data):
        str_pid = str(p_id)
        str_pid = '0' * (5 - len(str_pid)) + str_pid
        data = str_pid.encode(FORMAT) + data
        packets_dict[p_id] = data
        data = f.read(BUFFER_SIZE-5)
        p_id += 1

    print(len(packets_dict.keys()))
    print ("Sending ...")
 
    for pid in range(total_packets):
        server.sendto(packets_dict[pid], addr)
        packets += 1
        try:
            server.settimeout(0.01)
            data, addr = server.recvfrom(BUFFER_SIZE)
            ind = int(data.decode(FORMAT))
            ack[ind] = 1
        except socket.timeout:
            print("ACK not received")
            print(pid)
            continue

    print("Sent requested file")
    print(f"No. of packets sent: {packets}")
    print(f"No. of bytes sent: {file_size}")

    for i in range(len(ack)):
        if ack[i] == 0:
            print(i)

    time.sleep(20)
    f.close()

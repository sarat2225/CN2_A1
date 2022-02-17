import socket
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
BUFFER_SIZE = 4096
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"Server starting in {HOST}...")

while True:

    data, addr = server.recvfrom(BUFFER_SIZE)
    print(f"Requested file: {data.decode(FORMAT)}")

    file_name=data.decode(FORMAT)

    server.sendto(file_name.encode(FORMAT),addr)
    file_name = "udpuser\\" + file_name

    if not os.path.exists(file_name):
        print("Requested file doesn't exist")
        str = "NO"
        server.sendto(str.encode(FORMAT), addr)
        continue
    
    str = "YES"
    server.sendto(str.encode(FORMAT), addr)

    f=open(file_name,"rb")
    data = f.read(BUFFER_SIZE)
    packets = 0
    print ("Sending ...")
    while (data):
        if(server.sendto(data,addr)):
            packets += 1
            data = f.read(BUFFER_SIZE)
    print("Sent requested file")
    print(f"No. of packets sent: {packets}")
    print(f"No. of bytes sent: {os.path.getsize(file_name)}")
    f.close()
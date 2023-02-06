from socket import *
import json
import sys
import time
import os
import math
import threading

UDPPort = 12000
broadcastSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
broadcastSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

broadcastSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

chunkNames = {"chunks": []}

content_name = input('Please enter content name: ')
filename = content_name+'.png'
c = os.path.getsize(os.path.dirname(os.path.abspath(__file__)) + "/Images/" + filename)
print("Total size: ", c)
CHUNK_SIZE = math.ceil(math.ceil(c)/5)
print("Chunk size: ", CHUNK_SIZE)
index = 1
with open(os.path.dirname(os.path.abspath(__file__)) + "/Images/" + filename, 'rb') as infile:
    chunk = infile.read(int(CHUNK_SIZE))
    while chunk:
        chunkName = content_name+'_'+str(index)
        chunkNames["chunks"].append(chunkName)
        print("chunk name is: " + chunkName + "\n")
        with open(os.path.dirname(os.path.abspath(__file__)) + "/Images/" + chunkName, 'wb+') as chunk_file:
            chunk_file.write(chunk)
        index += 1
        chunk = infile.read(int(CHUNK_SIZE))
chunk_file.close()

print(chunkNames)

print("The server is ready to receive")

data = json.dumps(chunkNames)

print(data)
def Broadcast():
    while 1:
        broadcastSocket.sendto(data.encode("utf-8"), ('25.255.255.255', UDPPort))
        print('Broadcasted chunks.')
        time.sleep(60)

TCPport = 8000

UploadSocket = socket(AF_INET, SOCK_STREAM)
UploadSocket.bind(('', TCPport))
def Upload():
    while 1:
        print("Listening...\n")
        UploadSocket.listen()
        connectionSocket, addr = UploadSocket.accept()
        print("Connected.")

        fileData = json.loads(connectionSocket.recv(2048).decode("utf-8"))
        my_file = os.path.dirname(os.path.abspath(sys.argv[0])) + "/Images/" + fileData["requested_content"]
        file = open(my_file, 'rb')

        print("Sending...")

        data = file.read(2048)

        while data:
            connectionSocket.send(data)
            data = file.read(2048)

        print("Data sent.")
        file.close()
        connectionSocket.close()

BcastThread = threading.Thread(target=Broadcast)
BcastThread.start()
UploadThread = threading.Thread(target=Upload)
UploadThread.start()
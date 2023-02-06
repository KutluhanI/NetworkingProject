from socket import *
import json
import time
import os
import math

UDPPort = 12000
broadcastSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
broadcastSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

broadcastSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

chunkNames = {"chunks": []}

content_name = input('Please enter content name: ')
filename = content_name+'.png'
c = os.path.getsize(os.path.dirname(os.path.abspath(__file__))+ "/"+ filename)
print("Total size: ",c)
CHUNK_SIZE = math.ceil(math.ceil(c)/5)
print("Chunk size: ",CHUNK_SIZE)
index = 1
with open(os.path.dirname(os.path.abspath(__file__))+ "/"+ filename, 'rb') as infile:
    chunk = infile.read(int(CHUNK_SIZE))
    while chunk:
        chunkName = content_name+'_'+str(index)
        chunkNames["chunks"].append(chunkName)
        print("chunk name is: " + chunkName + "\n")
        with open(os.path.dirname(os.path.abspath(__file__))+ "/"+ chunkName,'wb+') as chunk_file:
            chunk_file.write(chunk)
        index += 1
        chunk = infile.read(int(CHUNK_SIZE))
chunk_file.close()

print(chunkNames)

print("The server is ready to receive")

data = json.dumps(chunkNames)

print(data)

while 1:
    time.sleep(10)
    broadcastSocket.sendto(data.encode("utf-8"), ('25.255.255.255', UDPPort))
    print('Broadcasted chunks.')
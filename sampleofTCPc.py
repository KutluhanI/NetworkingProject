from socket import *
import os
import json

serverPort = 8000

# receive file name
filename = input("Please enter the name of the file you wish to download: ")

requestedChunkNames = []

for i in range(1, 6):
    requestedChunkNames.append(filename + "_" + str(i))

for chunkName in requestedChunkNames:

    ##*lookup dictionary and get server name

    serverName = input("Enter ip to download: ")

    downloadSocket = socket(AF_INET, SOCK_STREAM)
    downloadSocket.connect((serverName, serverPort))

    fileData = {"requested_content": chunkName}

    downloadSocket.send(json.dumps(fileData).encode("utf-8"))

    newFile = open(os.path.dirname(os.path.abspath(__file__)) + "/Downloaded/" + chunkName, "wb")

    downloadedSize = 0
    print("Downloading" + chunkName + "...")

    data = downloadSocket.recv(2048)
    while data:
        downloadedSize += 2048
        newFile.write(data)
        print("File data recieved: " + str(downloadedSize))

        data = downloadSocket.recv(2048)
    print(chunkName + "done!")
    newFile.close()
    downloadSocket.close()
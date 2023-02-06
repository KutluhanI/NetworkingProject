from socket import *
import os
import json
import sys
import threading

UDPport = 12000
discoverySocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

discoverySocket.bind(('', UDPport))

print("Listening broadcast...")

contents = {}
def Discovery():
    while 1:
        data, conn = discoverySocket.recvfrom(2048)
        newd = json.loads(data.decode("utf-8"))
        print(newd)

        for i in newd["chunks"]:
            if i in contents.keys():
                if conn[0] not in contents[i]:
                    contents[i].append(conn[0])
            else:
                contents[i] = [conn[0]]

        deneme = json.dumps(contents)
        print(deneme)

TCPPort = 8000

requestedChunkNames = []
def Download():
    filename = input("Please enter the name of the file you wish to download: ")
    for i in range(1, 6):
        requestedChunkNames.append(filename + "_" + str(i))

    for chunkName in requestedChunkNames:
        ##*lookup dictionary and get server name
        i = 0
        TCPIP = contents[chunkName][i]
        #while not downloadSocket:
        #    try:
        #        downloadSocket = socket(AF_INET, SOCK_STREAM)
        #        downloadSocket.connect((TCPIP, TCPPort))
        #    except:
        #        i += i
        #        TCPIP = contents[chunkName][i]

        downloadSocket = socket(AF_INET, SOCK_STREAM)
        downloadSocket.connect((TCPIP, TCPPort))
        fileData = {"requested_content": chunkName}

        downloadSocket.send(json.dumps(fileData).encode("utf-8"))

        newFile = open(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Downloaded/" + chunkName, "wb")

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

DiscoveryThread = threading.Thread(target=Discovery)
DownloadThread = threading.Thread(target=Download)
DiscoveryThread.start()
DownloadThread.start()

import sys
import time
import threading
import json
import os
from socket import *
import math

UDPport = 5001
broadcastSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
broadcastSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
broadcastSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

chunkNames = {"chunks": []}

discoverySocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
discoverySocket.bind(('', UDPport))

TCPport = 8000
uploadSocket = socket(AF_INET, SOCK_STREAM)
uploadSocket.bind(('', TCPport))


def LogAdder(str: str):
    if not os.path.exists(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Log.txt"):
        log = open(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Log.txt", "w")
        log.write("[" + time.strftime("%H:%M:%S") + "]  " + str + "\n")
    else:
        log = open((os.path.dirname(os.path.abspath(sys.argv[0])) + "/Log.txt"), "a")
        log.write("[" + time.strftime("%H:%M:%S") + "]  " + str + "\n")


################################################### server ################################################################


def Broadcast():
    while 1:
        data = json.dumps(chunkNames)
        broadcastSocket.sendto(data.encode("utf-8"), ('25.255.255.255', UDPport))
        print('[UDP] Broadcasted chunks.')
        LogAdder('[UDP] Broadcasted chunks.')
        time.sleep(10)


def Upload():
    while 1:
        print("[TCP] Listening...\n")
        LogAdder('[TCP] Listening...')
        uploadSocket.listen()
        connectionSocket, addr = uploadSocket.accept()
        connectionSocket.settimeout(3)
        print("[TCP] Connected.")
        LogAdder('[TCP] Connected to the ' + addr[0])

        fileData = json.loads(connectionSocket.recv(2048).decode("utf-8"))
        filename = fileData["requested_content"]
        my_file = os.path.dirname(os.path.abspath(sys.argv[0])) + "/Contents/" + fileData["requested_content"]
        try:
            file = open(my_file, 'rb')
        except:
            print("[TCP] Could not read " + my_file)
            LogAdder("[TCP] Could not read " + my_file)

        print("[TCP] Sending...")
        LogAdder('[TCP] Sending the ' + filename + " to the " + addr[0])

        try:
            data = file.read(2048)
            while data:
                connectionSocket.send(data)
                data = file.read(2048)
        except:
            print("[TCP] Cannot send data to the" + addr[0])
            LogAdder("[TCP] Cannot send data to the" + addr[0])

        print("[TCP] Data sent.")
        LogAdder('[TCP] ' + filename + " has been sent to the " + addr[0])
        file.close()
        connectionSocket.close()


def ServerRun():
    contentIndex = input('Please enter the number of contents you wish to upload(type: int): ')
    while 1:
        try:
            val = int(contentIndex)
            break
        except ValueError:
            contentIndex = input('That is not an int. Please enter a valid index by type int: ')
    if val > 0:
        for i in range(val):
            content_name = input('Please enter content name: ')
            while 1:
                try:
                    filename = content_name + '.png'
                    c = os.path.getsize(os.path.dirname(os.path.abspath(__file__)) + "/Contents/" + filename)
                    print("Total size: ", c)
                    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
                    print("Chunk size: ", CHUNK_SIZE)
                    index = 1
                    with open(os.path.dirname(os.path.abspath(__file__)) + "/Contents/" + filename, 'rb') as infile:
                        chunk = infile.read(int(CHUNK_SIZE))
                        while chunk:
                            chunkName = content_name + '_' + str(index)
                            chunkNames["chunks"].append(chunkName)
                            print("chunk name is: " + chunkName + "\n")
                            LogAdder('Created ' + chunkName)
                            with open(os.path.dirname(os.path.abspath(__file__)) + "/Contents/" + chunkName,
                                      'wb+') as chunk_file:
                                chunk_file.write(chunk)
                            index += 1
                            chunk = infile.read(int(CHUNK_SIZE))
                    chunk_file.close()
                    break
                except:
                    content_name = input("[System] Data you have just entered does not exist or corrupted, please "
                                         "enter new one")
                    LogAdder('[System] A nonexistent or corrupted file has been entered. Requesting new one... ')

            print(chunkNames)

    print("[System] The server is ready to receive")

    BcastThread = threading.Thread(target=Broadcast)
    BcastThread.start()
    UploadThread = threading.Thread(target=Upload)
    UploadThread.start()


################################################### client ################################################################

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
        # deneme = json.dumps(contents)
        # print(deneme)


def Download():
    while 1:
        filename = input("Please enter the name of the file you wish to download: ")
        requestedChunkNames: list = []

        for i in range(1, 6):
            requestedChunkNames.append(filename + "_" + str(i))
        index = 0
        downloadedChunk = 0
        for chunkName in requestedChunkNames:
            ##*lookup dictionary and get server name
            try:
                lookupIp = contents[chunkName][index]
                print("[TCP] Connected to the" + lookupIp)
                fileData = {"requested_content": chunkName}
                downloadedSize = 0
                print("[TCP] Downloading " + chunkName + "...")
                LogAdder("[TCP] Downloading " + chunkName + "...")
                newFile = open(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Contents/" + chunkName, "wb")
                while index < len(contents[chunkName]):
                    try:
                        print("[TCP] Connecting to the " + lookupIp)
                        LogAdder("[TCP] Connecting to the " + lookupIp)
                        downloadSocket = socket(AF_INET, SOCK_STREAM)
                        downloadSocket.connect((lookupIp, TCPport))
                        downloadSocket.settimeout(1)
                        downloadSocket.send(json.dumps(fileData).encode("utf-8"))
                        data = downloadSocket.recv(2048)
                        while data:
                            downloadedSize += 2048
                            newFile.write(data)
                            print("[TCP] File data received: " + str(downloadedSize))
                            data = downloadSocket.recv(2048)
                        print(chunkName + " done!")
                        LogAdder("[TCP] File data received: " + str(downloadedSize))
                        LogAdder(chunkName + " has been downloaded from " + lookupIp)
                        downloadedChunk += 1
                        chunkNames["chunks"].append(chunkName)
                        newFile.close()
                        downloadSocket.close()
                        break
                    except:
                        downloadSocket.close()
                        print("[TCP] There was an error while downloading from address " + lookupIp)
                        LogAdder("[TCP] There was an error while downloading from address " + lookupIp)
                        index += 1
                        if index >= len(contents[chunkName]):
                            break
                        lookupIp = contents[chunkName][index]

                if index >= len(contents[chunkName]):
                    break
            except:
                print("Key you have just entered is wrong please enter new one.(Please select from the broadcasts by "
                      "online peers.)")
                LogAdder("Wrong key entered.")
                break
        if downloadedChunk == 5:
            FileAssembler(filename)
            print(filename + " done!")
            LogAdder(filename + " has been downloaded.")
        else:
            print("[Warning] " + filename + " cannot be downloaded from online peers, please select new content")
            LogAdder("[System] Cannot connect to any server, waiting for the new content request. ")


def FileAssembler(filename):
    with open(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Contents/" + filename + ".png", 'wb') as outfile:

        chunkNames = []

        for i in range(1, 6):
            chunkNames.append(filename + "_" + str(i))

        for chunk in chunkNames:
            with open(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Contents/" + chunk, 'rb') as infile:
                outfile.write(infile.read())
            infile.close()


def ClientRun():
    print("[System] Listening broadcast...")
    LogAdder("[System] Listening broadcast...")

    DiscoveryThread = threading.Thread(target=Discovery)
    DownloadThread = threading.Thread(target=Download)
    DiscoveryThread.start()
    DownloadThread.start()


#################################################### main ##################################################################

if not os.path.exists(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Contents/"):
    os.makedirs(os.path.dirname(os.path.abspath(sys.argv[0])) + "/Contents/")

ServerRun()
ClientRun()
from socket import *
import os
import json

port = 8000
UploadSocket = socket(AF_INET, SOCK_STREAM)
UploadSocket.bind(('', port))

while 1:
    UploadSocket.listen()

    print("Listening...")
    connectionSocket, addr = UploadSocket.accept()
    print("Connected.")

    fileData = json.loads(connectionSocket.recv(2048).decode("utf-8"))
    my_file = os.path.dirname(os.path.abspath(__file__)) + "/Images/" + fileData["requested_content"]
    file = open(my_file, 'rb')

    print("Sending...")

    data = file.read(2048)

    while data:
        connectionSocket.send(data)
        data = file.read(2048)

    print("Data sent.")
    file.close()
    connectionSocket.close()
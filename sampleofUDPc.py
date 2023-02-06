from socket import *
import json

serverIP: str = input('Please enter a host ip or host name: ')
UDPport = 12000
discoverySocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

discoverySocket.bind(('', UDPport))

print("Listening broadcast...")

contents = {}

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
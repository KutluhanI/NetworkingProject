This is the CMP2204 - 2021 Project made by Kutluhan İslim, Atila Doğu Sürücü, Cem Demir

This program is desined to download or upload chunks in peer-to-peer fashion among users. Users will broadcast the files they want to broadcast and
they recieve.Once they recieve a file requested by them, program will automatically broadcast it to the other users. We are using port 8000 for TCP and
5001 for UDP.

Please consider the following things in order to run the code properly;

-File you enter must be '.png' file without writing '.png'. We could make it send/recieve any file but we figured only .png files were mentioned
so we thought if we make it for only '.png' it'll be easier for users to use it. If you want to change the file type you recieve and send, you can
change the lines 87 and 203 "".png"" to what type you require to change it to.

-Chunks are broadcasted on '25.255.255.255' channel and 5001 port. If you cant get broadcasted chunks try broadcasting it on '<broadcast>' channel.

-If you try to send your files to yourself in the same computer you have to open two different directories, one for upload one for download in order to
download it without any corruptions because since the downloader creates new file chunks and uploader tries to get the information(bytes) from the 
requested chunk which will be new created one, there will be some corruptions and 0 byte files.

-We send and recieve datas in a while loop with 2048 bytes format. If you try to send or recieve the data with one shot (like if you make the format
20mil.) there will be some corruptions cause of sockets only recieve first 2048 bytes and still try to take furter, will eventually caught by timeout
function.


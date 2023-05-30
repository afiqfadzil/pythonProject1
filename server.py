import socket


serversocket = socket.socket()

host = 'localhost'
port = 54545


serversocket.bind(('', port))

serversocket.listen(1)

clientsocket,addr = serversocket.accept()
print("got a connection from %s" % str(addr))

while True:
    recv_msg = clientsocket.recv(1024)
    print(recv_msg.decode('utf-8'))
    send_msg = clientsocket.send(recv_msg)
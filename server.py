import socket

serversocket = socket.socket()

host = "localhost"
port = 54545
SERVER_ADDRESS = ("localhost", 54545)
serversocket.bind(SERVER_ADDRESS)

serversocket.listen(5)

while True:
    try:
        clientsocket, addr = serversocket.accept()
        print("got a connection from %s" % str(addr))
        while True:
            recv_msg = clientsocket.recv(1024)
            print(recv_msg.decode('utf-8'))
            send_msg = "S(OK)"
            clientsocket.send(str(send_msg).encode())
            if not recv_msg:
                print("Connection closed  due to  lack of data")
        clientsocket.close()
    except ConnectionResetError:
        print("Connection Reset, Waiting for new connection")

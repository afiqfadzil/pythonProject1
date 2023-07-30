import socket
import sys
from multiprocessing import Queue, Process

global response, command
response = Queue()
comm = Queue()
from time import sleep


def controller(response, comm):
    while True:
        control = comm.get()

        sleep(0.5)
        if control == "START":
            print("this is", control)
            r = Process(target=relay, args=(response,))
            r.start()
            r.join()
            r.terminate()
        elif control.isdigit() == True:
            print("this is 2nd", control)
            r = Process(target=relay, args=(response,))
            r.start()
            r.join()
            r.terminate()
            pass


def server(response, comm):
    serversocket = socket.socket()

    host = "localhost"
    port = 8000
    SERVER_ADDRESS = ("localhost", 8000)
    serversocket.bind(SERVER_ADDRESS)

    serversocket.listen(5)

    while True:
        try:
            clientsocket, addr = serversocket.accept()
            print("got a connection from %s" % str(addr))
            while True:
                recv_msg = clientsocket.recv(1024)
                print(recv_msg.decode('utf-8'))
                comm.put(recv_msg.decode('utf-8'))

                send_msg = response.get()
                print(send_msg)
                clientsocket.send(str(send_msg).encode())
                if not recv_msg:
                    print("Connection closed  due to  lack of data")
            clientsocket.close()
        except ConnectionResetError:
            print("Connection Reset, Waiting for new connection")


def relay(response):
    while True:
        response.put("OK")
        break


if __name__ == '__main__':
    c = Process(target=controller, args=(response, comm,))
    s = Process(target=server, args=(response, comm,))

    s.start()
    c.start()

    pass

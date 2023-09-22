import socket
from multiprocessing import Queue, Process
from time import sleep

response = Queue()
comm = Queue()
data = Queue()

OK = "OK"


def controller(response, comm, data):
    while True:
        control = comm.get()

        sleep(0.5)
        if control == "START":
            print("this is", control)
            control = comm.get()
            if control.isdigit():
                print("this is 2nd", control)
                data.put(control)
                r = Process(target=relay, args=(response, data))
                r.start()
                r.join()
                r.kill()
                print("PROCESS COMPLETED")
                sleep(0.5)
            elif control == "EXIT":
                response.put("OK")
                print("EXIT SUCCESS")
            else:
                pass



        elif control == "ONETIMEREAD":
            m = Process(target=maintenance, args=(response, data))
            m.start()
            m.join()
            m.terminate()
            send = data.get()
            response.put(send)
            print("PROCESS COMPLETED")



        elif control == "EXIT":
            response.put("OK")
            print("EXIT SUCCESS")


        else:

            response.put("OK")
            print("EXIT SUCCESS")


def maintenance(response, data):
    data.put("READING IS XX")

    pass


def server(response, comm):
    serversocket = socket.socket()

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
            clientsocket.close()


def relay(response, data):
    seat = data.get()  # retrieve seat height form data.Queue()
    print("Seat Height is", seat)
    response.put("OK")


if __name__ == '__main__':
    c = Process(target=controller, args=(response, comm, data,))
    s = Process(target=server, args=(response, comm,))

    s.start()
    c.start()

    pass

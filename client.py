import socket


class MySocket:

    #def __init__(self, host="133.54.230.187", port=8000):
    def __init__(self, host="localhost", port=54545):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        print("Connected")


    def get_data(self):
        recv_msg = self.sock.recv(1024)
        return recv_msg

    def send_data(self, send_msg):
        self.sock.send(send_msg.encode())

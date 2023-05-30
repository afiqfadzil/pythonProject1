import socket


class MySocket:

    def __init__(self, host="localhost", port=54545):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        print("Connected")

    def get_data(self):
        return self.sock.recv(1024)

    def send_data(self,send_msg):

        return self.sock.send(str(send_msg).encode())

import socket


class MySocket:

    #def __init__(self, host="133.54.230.189", port=8000):
    def __init__(self, host, port=8000):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.sock.connect((host, port))
        self.sock.settimeout(15)

        print("Connected")


    def get_data(self):
        recv_msg = self.sock.recv(1024)
        return recv_msg

    def send_data(self, send_msg):
        self.sock.send(send_msg.encode())

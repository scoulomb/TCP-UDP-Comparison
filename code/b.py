import random
import socket
import time


def main_tcp():
    with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s):
        s.connect(("localhost", 7777))
        s.sendall(b"from B")
        while True:
            data = s.recv(1024)
            print("message: %s" % data)
            time.sleep(1)
            s.sendall(b"got something")
            if random.Random().randint(0, 100) > 99:
                s.sendall(b"stop")
            if data == b"stop":
                print("asked to stop, disregarding")
                while True:
                    s.sendall(b"live!")
                    time.sleep(1)

def main_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b"from B", ("localhost", 7777))
        while True:
            data, addr = s.recvfrom(1024)
            print("message: %s" % data)
            time.sleep(1)
            s.sendto(b"got something", addr)
            if random.Random().randint(0, 100) > 80:
                s.sendto(b"stop", addr)
            if data == b"stop":
                print("asked to stop, disregarding")
                while True:
                    s.sendto(b"live!", addr)
                    time.sleep(1)


if __name__ == "__main__":
    print("I am a client")
    main_udp()
    #main_tcp()

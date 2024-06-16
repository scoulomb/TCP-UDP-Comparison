import socket
import time
from concurrent.futures import ThreadPoolExecutor


def handle_connection(conn):
    while True:
        data = conn.recv(1024)
        print("message: %s" % data)
        time.sleep(1)
        conn.sendall(b"thanks")
        if data == b"stop":
            conn.sendall(b"stop")
            exit(0)

def main_tcp():
    # AF_INET == IPv4
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 7777))
        s.listen()
        while True:
            conn, addr = s.accept()
            POOL.submit(handle_connection, conn)

def main_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('localhost', 7777))
        while True:
            data, addr = s.recvfrom(1024)
            print("message: %s" % data)
            time.sleep(1)
            s.sendto(b"thanks", addr)
            if data == b"stop":
                s.sendto(b"stop", addr)
                exit(0)


if __name__ == "__main__":
    print("I am server")
    global POOL
    POOL = ThreadPoolExecutor(max_workers=5)

    main_udp()
    #main_tcp()

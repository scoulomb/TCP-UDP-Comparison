# Comparison of TCP and UDP


## Run our test

Uncomment `main_tcp()` or `main_udp()`.

````
cd code
python3 a.py
python3 b.py
python3 c.py
````


<!-- https://stackoverflow.com/questions/19742345/what-is-the-format-for-date-parameter-of-git-commit -->

## Analysis


### [Server](a.py)

In `TCP` server is doing on socket `s`

````
s.bind(('localhost', 7777))
s.listen()
conn, addr = s.accept() # Manage in a threadpool to handle multiple connection
conn.recv(1024)
conn.sendall(b"thanks")
````


whereas in `UDP` 


````
s.bind(('localhost', 7777))
data, addr = s.recvfrom(1024)
s.sendto(b"thanks", addr)
````

### [Client](b.py)


In TCP client is doing on socket `s`

````
s.connect(("localhost", 7777)) -- link to accept on TCP server
s.sendall(b"from B")
data = s.recv(1024)          
````

In UDP client is doing

````
s.sendto(b"from B", ("localhost", 7777))
data, addr = s.recvfrom(1024)
s.sendto(b"got something", addr)
````

Which is matching III-E. Récapitulatif at https://broux.developpez.com/articles/c/sockets/

### Difference between UDP and TCP.

Note in `UDP` server has to do the `bind`.
But client can also do it: https://stackoverflow.com/questions/41582107/can-i-bind-a-client-socket-to-an-ip-not-belongs-to-any-interfaces
It will just force a specific source IP in UDP datagram.


As a conclusion there is no socket establishment direction in UDP unlike TCP.
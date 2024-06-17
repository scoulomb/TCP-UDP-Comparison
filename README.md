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

So in [b.py`main_udp`](./code/b.py) we can perform `s.bind(('localhost', 6666))` 
It will just force a specific source IP in UDP datagram.

If we do a packet capture with `sudo wireshark` on `lo1`, we will see source IP is `6666` whereas otherwise it is randomly chosen.

As a conclusion there is no socket establishment direction in UDP unlike TCP.

Note if `a (server)` is not doing the bind,  `b (client)`  can not know the port to target.
When `b` is answering to `a`, it uses the source IP in `a` UDP datagram.

In context of UDP we use client/server but there is not really strong client/server concept as in TCP.
Since there is no difference between `a` and `b` in the end.


https://github.com/scoulomb/private_script/blob/main/Links-mig-auto-cloud/Additional-comments.md#socket-establishment-directrion-vs-message-flow-direction
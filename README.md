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
But `UDP` client can also do it: https://stackoverflow.com/questions/41582107/can-i-bind-a-client-socket-to-an-ip-not-belongs-to-any-interfaces

So in [b.py`main_udp`](./code/b.py) we can perform `s.bind(('localhost', 6666))` 
It will just force a specific source IP in UDP datagram.

If we do a packet capture with `sudo wireshark` on `lo1`, we will see source IP is `6666` whereas otherwise it is randomly chosen.

Obviously same is possible in `TCP` client.
So in [b.py`main_tcp`](./code/b.py) we can perform `s.bind(('localhost', 5555))
Also verified via Wireshark.
 

Note if `a (server)` is not doing the bind (UDP and TCP),  `b (client)`  can not know the port to target.
When `a` is answering to `b`: (also visibe via Wireshark)
````
Wireshark pcap

User Datagram Protocol, Src Port: 38121, Dst Port: 7777 (b->a)
User Datagram Protocol, Src Port: 7777, Dst Port: 38121 (a->b)
````
- it uses the destination (IP, Port) in `b` UDP datagram source (IP,Port) 
- it uses the source (IP, Port) in `a` UDP datagram destination (IP, Port) : the one we bind on server side

Last one has an importance in restrcited cne NAT, Port restricted cone NAT and symetric NAT.

See
- http://wapiti.enic.fr/commun/ens/peda/options/ST/RIO/pub/exposes/exposesrio2005/cleret-vanwolleghem/nat.htm
- https://github.com/scoulomb/home-assistant/blob/main/appendices/VPN-tailscale.md


API is not consitent in TCP `recv` is done on `conn` object on server side, whereas done on socket in client side.


Unlike in TCP, in context of UDP we use client/server but there is not really strong concept of client/server.
UDP Server is usually doing the bind and client is sending the first message (server replies using  source (ip, port) in client packet), and we saw client can also do the bind. 

**Therefore our  conclusion is that socket establishment direction is a `TCP` concept**

[here]

add link to raw socket
https://github.com/scoulomb/private_script/blob/main/Links-mig-auto-cloud/Additional-comments.md#socket-establishment-directrion-vs-message-flow-direction
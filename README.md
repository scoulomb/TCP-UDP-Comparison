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

Note in `UDP` server has still to do the `bind`.
But `UDP` client can also do it: https://stackoverflow.com/questions/41582107/can-i-bind-a-client-socket-to-an-ip-not-belongs-to-any-interfaces

So in [b.py`main_udp`](./code/b.py) we can perform `s.bind(('localhost', 6666))` 
It will just force a specific source IP in UDP datagram.
If we do a packet capture with `sudo wireshark` on `lo1`, with `s.bind(('localhost', 6666))`  on client, we will see source IP is `6666` whereas otherwise it is randomly chosen.

Obviously `TCP` client can also do the `bind`.
So in [b.py`main_tcp`](./code/b.py) we can perform `s.bind(('localhost', 5555))
Also verified same behavior via Wireshark.
 

Note if `a (server)` is not doing the bind (UDP and TCP),  `b (client)`  can not know which port to target.
When `a` is answering to `b`: (also visibe via Wireshark)

````
Wireshark pcap

User Datagram Protocol, Src Port: 38121, Dst Port: 7777 (b->a) 
User Datagram Protocol, Src Port: 7777, Dst Port: 38121 (a->b)
````
- it uses as destination (IP, Port), the one in `b->a` UDP datagram source (IP,Port) 
- it uses as source (IP, Port), the one in `b->a`  UDP datagram destination (IP, Port) : the one we bind on server side

`b->a` source port has an importance in `Port Restricted Cone NAT`, and `symetric NAT`.

See
- http://wapiti.enic.fr/commun/ens/peda/options/ST/RIO/pub/exposes/exposesrio2005/cleret-vanwolleghem/nat.htm
- https://github.com/scoulomb/home-assistant/blob/main/appendices/VPN-tailscale.md


API is not consitent in TCP `recv` is done on `conn` object on server side, whereas done on socket in client side.


Unlike in TCP, in context of UDP we use client/server terminology but there is not really strong concept of client/server, as there is no socket establishment direction as such.
However, what we can see as "UDP Server", HAS TO do the bind and what we see as b (server replies using  destination (ip, port) in client source packet (and we saw client can also do the bind).

To be more exact <!-- comment JM and totally well integrated -->
> C'est pas totalement vrai que le client doit envoyer le premier message.
> Si le client et le server se sont mis d'accord en avance sur le port (ou il a ete decouvert par un autre moyen), alors le server ou le client peut commencer sans soucis.
> Mais de maniere generale, c'est vrai que c'est plus courant que le client initie
In that case what we see as "client" has to do the bind and it totally removes the concept of client/server in UDP! 


**Therefore our  conclusion is that socket establishment direction is more a `TCP` concept**.


## TCP Socket establishment direction 


- TCP **Socket establishment direction** is inbound (and we are server) if on our end/entity (1A, corpo) we do
    - s.bind
    - s.listen
    - s.accept
- else TCP socket easblishment is outbound (and we are client), on our end/entity we do
   - s.connect -- link to accept on TCP server


- We can extend to UDP client/server where we consider server (when port is not communicated via other mechanism)
    - The part which HAS TO do the bind (as seen above both client/server can do it),
-  and client
    - Part sending first message 
    

- **Message flow direction is***
    - outound for entity sending the query, and receiving the reply
    - inbound for entity receiving the query, and sending the reply 

Please note that  Message flow direction != TCP Socket establishment direction, see: /private_script/blob/main/Links-story-notes/socketEstablishmentDirection.md
And as in this example message flow direction can be bi-directionnal. (Comment: For UDP, client still has to send first message)

Usually message flow direction same as TCP socket establishment direction (for example we query an API). 
Example when not in same direction is push notification: from mobile device perspective TCP socket establishment is outbound, message flow is inbound.


This same mechanism (where socket establishment is outbound and message flow inbound for home user) is heavily used by smarthome devices like Hue, Netatmo, Somfy Tahoma, Apple Home (to local HUE via HomeKit)

Instead of having a NAT rule to access internal API (or VPN): `Client->  IP public -> NAT -> Hue hub`
https://github.com/scoulomb/myhaproxy/blob/main/README.md#we-have-seen-3-ways-to-access-internal-server-from-external (See also tailscale VPN which enables to traverse NAT without NAT rules: https://github.com/scoulomb/home-assistant/blob/main/appendices/VPN-tailscale.md)


What they are doing is : `Client -> HUE cloud <- Hub HUE` (arrow are socket establishment direction)


````
Hub HUE do outbound sokect establishment to HUE cloud (TCP socket permanent keep alive)
If input 
		HUEcloud.socket.send(toHubHue) 
````

Alternative is: connected devices (Hue, Netatmo...) can perform conitnous polling (CURL GET) to the server until ITO rather than keeping socket open. When server has data it sends the data. It means device is still opening the socket. This is what is also used by chat, they do a poll to central server to receive message. 
(Except ms teams where robotic user where here server is pushing (it means teams server doing inbound socket establishment to chat client)) <!-- michel -->


Or we do

````
HUBHue doing curl to HUECloud
While True:
	curl -X GET huecloud.com/events: return payload with list of actions

````

In the 2 alternative note we come back in a case where socket establishment direction == nessage flow, and device at home doing outbound socket establishment


- Also not for Internet provider only **packet direction** is counting in their upload speed:
    - Upload speed (debit montant): uplaod a file, download a file in a Natted server at home: https://github.com/scoulomb/home-assistant/blob/main/sound-video/setup-your-own-media-server-and-music-player/README.md 
    - Downlaod speed (debit descendant): dowanload a file on internet, what a netflix move
- ADSL optimizes the download speed thus asymetric and slow Jellyin donwload speed (from mobile client perspective, where socket establishment + message direction is inbound but big packt in reply are outbound)


<!-- here -- all above is OK -->


## Network devices and socket establishment


In term of network setup usually
- Outbound socket establishment entity usually exposes a SNAT facade (IP, Port) through SNAT policy on Firewall/Loadbalancer, and filter the traffic via filtering rules on firewall
- Inbound socket establishment entity has Filtering rules on firewall accepting traffic from SNAT facade (IP) to destination (IP, Port). It listens traffic on destination (IP, Port). 
    - Listen can be 
        - on Firewall (requires a routing rules for router to FW, back to router then router to LB)
        - or LoadBalancer (requires a DNAT from fw to LB)

<!--
- See link with 
    - private_script/blob/main/Links-mig-auto-cloud/listing-use-cases/listing-use-cases.md#ip-used-in-outbound-only-socket-establishment-case-where-legacy-datacenter-f5-wasis-involved
    - private_script/blob/main/Links-mig-auto-cloud/README.md#migration-and-snatdnat (Design v1/v2)
-->

When a packet is going out firewall accepts the response of packet coming back, see https://github.com/scoulomb/home-assistant/blob/main/appendices/VPN-tailscale.md 


And this is used by:  https://github.com/scoulomb/home-assistant/blob/main/appendices/VPN-tailscale.md 


## VPN IP as SNAT facade


Also in corpo network, when no VPN is put in place between employee laptop and corporate network (vpn used connect to remote local network) for example a git server), we need to open firewall to have source IP of the employee allowed (inbound establishment to corpo). It can be the NAT IP of the box. VPN with static IP adress can help to always go out with same IP (VPN used for SNAT). Practical if client moving or using 4g device

See https://github.com/scoulomb/home-assistant/blob/main/appendices/VPN.md#into (remote local nw and snat : Client -> VPN TUNNEL -> LAN -> SNAT ) See also link with https://github.com/scoulomb/home-assistant/blob/main/appendices/VPN.md#alternative


Referenced in /private_script/blob/main/Links-mig-auto-cloud/Additional-comments.md#socket-establishment-directrion-vs-message-flow-direction

## Links with HTTP over socket

https://github.com/scoulomb/http-over-socket/tree/main: where we had also implemented a HTTP client/server over TCP. 

<!--quic udp etc -- skip -->
import socket
import time
import struct

PORT = 5007
MCAST_GRP = "ff02::1"
INTERFACE = "eth0"

def receive_messages():

   sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

   try:
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
   except AttributeError:
      print("SO_REUSEPORT is not available on this system.")
   sock.bind(("", PORT))

   group = socket.inet_pton(socket.AF_INET6, MCAST_GRP)
   mreq = group + struct.pack("@I", socket.if_nametoindex(INTERFACE))
   sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

   received_packets = 0
   total_bytes_received = 0
   start_time = None

   print(f"Listening for IPv6 messages on port {PORT}...")

   while True:
       data, addr = sock.recvfrom(1024)
       received_time = time.time()
       received_packets = data.decode()
       total_bytes_received += len(data)

       sent_time = float(data.decode().split("|")[1])
       latency = received_time - sent_time

       if received_packets == 1:
           start_time = received_time

       print(f"Received packet {received_packets} from {addr}, Latency: {latency:.6f} s")

       sock.sendto(b"Received the message!", addr)

   sock.close()

if __name__ == "__main__":
   receive_messages()
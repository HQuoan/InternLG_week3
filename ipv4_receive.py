import socket
import time
import struct

PORT = 5007
MCAST_GRP = "224.0.0.1"
INTERFACE = "eth0"

def receive_messages():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    received_packets = 0
    start_time = None
    total_bytes_received = 0

    print(f"Listening for messages on port {PORT}...")

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
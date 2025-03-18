import socket
import time

MCAST_GRP = "ff02::1"
PORT = 5007
INTERFACE = "eth0"
NUM_PACKETS = 1000

def send_messages(target_ip, multicast=False, unicast=False):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    if multicast:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 2)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, socket.if_nametoindex(INTERFACE))

    try:
        while True:
            sent_packets = 0
            received_messages = 0
            total_bytes_sent = 0

            message = input("Enter message (type 'exit' to return to menu): ").strip()
            if message.lower() == "exit":
                break
            start_time = time.time()

            print(f"Simulate sending the message {message} {NUM_PACKETS} times...")
            for i in range(NUM_PACKETS):
                new_message = f"{message} Packet {i+1}|{time.time()}"
                sock.sendto(new_message.encode(), (target_ip, PORT))
                sent_packets += 1
                total_bytes_sent += len(new_message)

                sock.settimeout(0.02)
                while True:
                    try:
                        response, _ = sock.recvfrom(1024)
                        received_messages += 1
                    except socket.timeout:
                        break

            end_time = time.time()
            duration = end_time - start_time
            throughput = total_bytes_sent / duration if duration > 0 else 0

            print("\n--- Performance Report ---")
            print(f"Packets Sent: {sent_packets}")
            print(f"Packets Received: {received_messages}")
            print(f"Total Bytes Sent: {total_bytes_sent} bytes")
            print(f"Duration: {duration:.6f} s")
            print(f"Throughput: {throughput:.2f} bytes/s")

    except KeyboardInterrupt:
        print("\nStopping sender...")
    finally:
        sock.close()

if __name__ == "__main__":
    while True:
        print("\n--- Choose options ---")
        print("1. Unicast")
        print("2. Multicast")
        print("3. Anycast (simulate as Unicast)")
        print("4. Exit")

        choice = input("Choose (1/2/3/4): ").strip()

        if choice == "1":
            target_ip = input("Enter IPv6 Unicast target: ").strip()
            send_messages(target_ip, unicast=True)
        elif choice == "2":
            send_messages(MCAST_GRP, multicast=True)
        elif choice == "3":
            target_ip = input("Enter IPv6 Anycast target (simulate as Unicast): ").strip()
            send_messages(target_ip, unicast=True)
        elif choice == "4":
            print("Exiting!")
            break
        else:
            print("Invalid choice!")
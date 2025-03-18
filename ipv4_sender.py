import socket
import time

MCAST_GRP = "224.12.1.1"
PORT = 5007
BROADCAST_IP = "10.12.2.255"
NUM_PACKETS = 1000
INTERFACE = "eth0"

def send_messages(target_ip, multicast=False, broadcast=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    if multicast:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    if broadcast:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, 25, INTERFACE.encode())


    try:
      while True:
        sent_packets = 0
        received_message = 0
        total_bytes_sent = 0
        message = input("Enter message (type 'exit' to return to menu): ").strip()
        if message.lower() == "exit":
          break
        start_time = time.time()

        print(f"Simulate sending the message {message} {NUM_PACKETS} times...")
        for i in range(NUM_PACKETS):
            new_message = message + f" Packet {i+1}|{time.time()}"
            sock.sendto(new_message.encode(), (target_ip, PORT))
            sent_packets += 1
            total_bytes_sent += len(new_message)

            sock.settimeout(0.02)
            while True:
                try:
                    response, _ = sock.recvfrom(1024)
                    received_message += 1
                except socket.timeout:
                    break

        end_time = time.time()
        duration = end_time - start_time
        throughput = total_bytes_sent / duration

        print("\n--- Performance Report ---")
        print(f"Packets Sent: {sent_packets}")
        print(f"Packets Received: {received_message}")
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
        print("1. Unicast ")
        print("2. Multicast")
        print("3. Broadcast")
        print("4. Exit")
        choice = input("Choose (1/2/3/4): ").strip()

        if choice == "1":
            target_ip = input("Type IP target: ").strip()
            send_messages(target_ip)
        elif choice == "2":
            send_messages(MCAST_GRP, multicast=True)
        elif choice == "3":
            send_messages(BROADCAST_IP, broadcast=True)
        elif choice == "4":
            print("Exit!")
            break
        else:
            print("Invalid choice!")
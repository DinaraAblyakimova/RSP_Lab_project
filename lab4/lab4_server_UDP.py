# server_udp.py
import socket
import struct

MULTICAST_GROUP = '233.0.0.1'
PORT = 1502

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

    print("UDP сервер запущен. Введите сообщение для отправки клиентам:")

    try:
        while True:
            message = input("> ")
            if not message:
                continue
            sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))
            print(f"Отправлено: {message}")
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()

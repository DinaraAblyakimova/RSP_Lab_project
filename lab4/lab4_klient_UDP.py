# client_udp.py
import socket
import struct

MULTICAST_GROUP = '233.0.0.1'
PORT = 1502

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))  

    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Клиент запущен. Ожидание сообщений от сервера...")

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Получено сообщение от {addr}: {data.decode().strip()}")
    except KeyboardInterrupt:
        print("\nКлиент остановлен.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()

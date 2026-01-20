# server_tcp.py
import socket
import threading
import datetime
import pickle

HOST = '192.168.0.110'
# HOST = 'localhost'
PORT = 1501

def handle_client(conn, addr):
    print(f"Подключение от {addr}")
    message = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Привет время сейчас у нас "
    }
    data = pickle.dumps(message)  
    conn.sendall(data)
    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"TCP сервер запущен на порту {PORT}...")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.close()

if __name__ == "__main__":
    main()

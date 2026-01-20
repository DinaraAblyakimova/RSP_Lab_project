# client_tcp.py
import socket
import pickle

# HOST = 'localhost'
HOST = '192.168.0.110'
PORT = 1501

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    data = client.recv(1024)
    message = pickle.loads(data)  # десериализация объекта

    print(message["message"])
    print(message["date"])

    client.close()

if __name__ == "__main__":
    main()

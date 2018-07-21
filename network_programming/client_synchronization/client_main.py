import socket
import time


HOST = "127.0.0.1"
PORT = 7777
NODE_ID = "1"


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    while True:
        # time.sleep(int(NODE_ID))
        client_socket.send(NODE_ID.encode("ascii"))
        data = client_socket.recv(1024)
        random_seed = data.decode("ascii")
        print(NODE_ID, random_seed)
    client_socket.close()


if __name__ == "__main__":
    main()

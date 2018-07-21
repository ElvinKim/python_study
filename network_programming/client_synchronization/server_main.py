import socket
from _thread import *
import threading
import random


HOST = ""
PORT = 7777
RANDOM_SEED = 0
REC_NODE_LST = []
NUM_WORK_NODES = 3


def handle_client_socket(c, cond_var):
    while True:

        data = c.recv(1024)
        if not data:
            break
        data = data[::-1]
        REC_NODE_LST.append(str(data).strip())

        with cond_var:
            cond_var.wait()
        c.send(str(RANDOM_SEED).encode('ascii'))
    c.close()


def control_thread_schedule(cond_var):
    print("[start]\tcontrol_thread_schedule thread")
    global RANDOM_SEED
    while True:
        temp_lst = list(set(REC_NODE_LST))
        if len(temp_lst) == NUM_WORK_NODES:
            RANDOM_SEED = random.randint(1, 1000000000)
            REC_NODE_LST.clear()
            with cond_var:
                cond_var.notifyAll()


def main():
    cond_var = threading.Condition()
    start_new_thread(control_thread_schedule, (cond_var,))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        try:
            client, addr = server_socket.accept()
            print("[connection]", client)
            start_new_thread(handle_client_socket, (client, cond_var,))
        except Exception as e:
            print(e)
            server_socket.close()


if __name__ == "__main__":
    main()


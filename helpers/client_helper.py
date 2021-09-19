import socket
import threading

from settings import HOST, PORT


def receive(nickname: str, client: socket):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break


def write(nickname: str, client: socket):
    while True:
        message = input('')
        client.send(message.encode('ascii'))


def start_client():
    nickname = input("Choose your nickname: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    receive_thread = threading.Thread(target=receive, args=(nickname, client))  # receiving multiple messages
    receive_thread.start()
    write_thread = threading.Thread(target=write, args=(nickname, client))  # sending messages
    write_thread.start()

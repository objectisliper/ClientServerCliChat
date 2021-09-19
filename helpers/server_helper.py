import socket
import threading

from settings import HOST, PORT
from datetime import datetime

clients = []
nicknames = []
message_history = []


def broadcast(message):
    message = datetime.now().strftime('%H:%M:%S').encode('ascii') + b' => ' + message
    message_history.append(message)
    for client in clients:
        client.send(message)


def get_client_nickname(client):
    index = clients.index(client)
    nickname = nicknames[index]
    return nickname


def handle(client):
    while True:
        nickname = get_client_nickname(client)

        try:
            message = client.recv(1024)
            if len(message) > 0:
                broadcast(f'{nickname}: {message.decode("ascii")}'.encode('ascii'))
        except:
            clients.remove(client)
            client.close()
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)

            break


def restore_message_history(client):
    client.send(b'\n'.join(message_history) + b'\n')


def client_init(client):
    client.send('NICKNAME'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')
    nicknames.append(nickname)
    clients.append(client)
    print("Nickname is {}".format(nickname))
    restore_message_history(client)
    broadcast("{} joined!".format(nickname).encode('ascii'))


def event_loop_init(client):
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client_init(client)
        event_loop_init(client)



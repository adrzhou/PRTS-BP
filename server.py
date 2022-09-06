import socket
from time import sleep
from threading import Thread
from random import shuffle
from typing import List

PORT = 5050
rooms = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")
server.bind(('', PORT))
print(f"Socket bound to port {PORT}")
server.listen()
print("Socket is listening")


def handle_client(client: socket.socket, addr):
    print(f'Got connection from {addr}')
    client.send(b'CONNECTED')
    room = client.recv(64).decode()
    if room not in rooms:
        rooms[room] = [client]
        client.send(b'CREATED')
    elif len(rooms[room]) == 2:
        client.send(b'FULL')
        return
    else:
        rooms[room].append(client)
        client.send(b'JOINED')

    if len(rooms[room]) == 2:
        session(rooms[room])


def session(room: List[socket.socket]):
    shuffle(room)
    first, second = tuple(room)
    first.send(b'FIRST')
    second.send(b'SECOND')
    sleep(1)

    def ban(client):
        if client is first:
            opponent = second
        else:
            opponent = first

        client.send(b'BAN')
        opponent.send(b'BANNING')
        response = client.recv(64)
        opponent.send(response)
        confirmation = opponent.recv(64)
        client.send(confirmation)

    def pick(client):
        if client is first:
            opponent = second
        else:
            opponent = first

        client.send(b'PICK')
        opponent.send(b'PICKING')
        response = client.recv(64)
        opponent.send(response)
        confirmation = opponent.recv(64)
        client.send(confirmation)

    # Rule reference: BV1tL41157wW
    for _ in range(3):
        ban(first)
        ban(second)
    order = (first, second, second, first, first, second)
    for _ in range(2):
        for player in order:
            pick(player)
    for _ in range(2):
        ban(second)
        ban(first)
    order = (second, first, first, second, second, first)
    for _ in range(2):
        for player in order:
            pick(player)

    sleep(2)
    first.send(b'QUIT')
    second.send(b'QUIT')
    first.close()
    second.close()
    room.clear()


while True:
    c = Thread(group=None, target=handle_client, args=(server.accept()))
    c.start()

import socket


SERVER_IP: str = ''
PORT: int = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

assert client.recv(64) == b'CONNECTED'
print('Connected to server')

room = 'test'
client.send(room.encode())
match [client.recv(64)]:
    case [b'CREATED']:
        print(f'Created a new room named {room}')
    case [b'FULL']:
        print('Room is full')
    case [b'JOINED']:
        print(f'Joined room {room}')
    case _:
        raise Exception

match [client.recv(64)]:
    case [b'FIRST']:
        first = True
        print('You ban first')
    case [b'SECOND']:
        first = False
        print('Opponent bans first')
    case [catch]:
        print(catch.decode())
        raise Exception

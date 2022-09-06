from threading import Thread, Event
from client import client
from picked import Picked, Banned
from selector import ConfirmButton, Pool
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

app = QApplication([])
confirm = ConfirmButton()
pool = Pool(confirm)
left_banned = Banned('left')
right_banned = Banned('right')
left_picked = Picked('left')
right_picked = Picked('right')

selector = QWidget()
selector.setLayout(QVBoxLayout())
selector.layout().addWidget(pool)
selector.layout().addWidget(confirm)

bottom = QWidget()
bottom.setLayout(QHBoxLayout())
bottom.layout().addWidget(left_picked)
bottom.layout().addWidget(selector)
bottom.layout().addWidget(right_picked)

top = QWidget()
top.setLayout(QHBoxLayout())
top.layout().addWidget(left_banned)
top.layout().addWidget(QWidget())
top.layout().addWidget(right_banned)

main = QWidget()
main.setFixedSize(1600, 900)
main.setLayout(QVBoxLayout())
main.layout().addWidget(top)
main.layout().addWidget(bottom)
main.show()


def client_thread():
    def request_ban(event, a_payload):
        confirm.t_event = event
        confirm.payload = a_payload
        confirm.setText('禁用')
        confirm.setEnabled(True)

    def request_pick(event, a_payload):
        confirm.t_event = event
        confirm.payload = a_payload
        confirm.setText('选用')
        confirm.setEnabled(True)

    while True:
        match client.recv(64).decode().split():
            case ['BAN']:
                e = Event()
                payload = ['']
                ban_thread = Thread(target=request_ban, args=[e, payload])
                ban_thread.start()
                e.wait()
                op: str = payload[0]
                client.send(f'BANNED {op}'.encode())
                assert client.recv(64) == b'CONFIRMED'
                left_banned.ban(op)
                if 'no_select' not in op:
                    pool.all[op].setEnabled(False)
            case ['BANNING']:
                confirm.setText('敌方正在禁用干员...')
            case ['BANNED', op]:
                right_banned.ban(op)
                if 'no_select' not in op:
                    pool.all[op].setEnabled(False)
                client.send(b'CONFIRMED')
            case ['PICK']:
                e = Event()
                payload = ['']
                pick_thread = Thread(target=request_pick, args=[e, payload])
                pick_thread.start()
                e.wait()
                op: str = payload[0]
                client.send(f'PICKED {op}'.encode())
                assert client.recv(64) == b'CONFIRMED'
                left_picked.pick(op)
                if 'no_select' not in op:
                    pool.all[op].setEnabled(False)
            case ['PICKING']:
                confirm.setText('敌方正在选用干员...')
            case ['PICKED', op]:
                right_picked.pick(op)
                if 'no_select' not in op:
                    pool.all[op].setEnabled(False)
                client.send(b'CONFIRMED')
            case ['QUIT']:
                client.close()
                break
            case _:
                raise Exception


t = Thread(target=client_thread)
t.start()

app.exec()

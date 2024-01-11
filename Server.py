import socket
from _thread import *
import sys

server = socket.gethostname()
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0),(100,100)]
action= "Random"
def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    global action

    while True:
        try:
            if player ==1:
                data = conn.recv(2048).decode()
                action = data
            else:
                data = read_pos(conn.recv(2048).decode())
                pos[player] = data


            if not data :
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = make_pos(pos[0])
                else:
                    reply = action

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except Exception as inst:
            print(type(inst))    # the exception type
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
                                 # but may be overridden in exception subclasses
            x, y = inst.args     # unpack args
            print('x =', x)
            print('y =', y)
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

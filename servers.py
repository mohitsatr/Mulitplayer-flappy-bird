import pickle 
import socket

from _thread import start_new_thread
from client import Player 
import keyboard
from box import Bird

window_width = 370
window_height = 400


HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on (non-privileged ports are > 1023)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


def start():
    s.bind((HOST, PORT))
    s.listen()
    print("Server started waiting for new connection : ...")

# PlayersList = [
#     Player("Mohit"), Player("Raj")
# ]
initial_position = window_width//2.5,window_height//2.5


Pos = [(initial_position),(initial_position)]


def threaded_client(player,conn,addr):
    conn.send(pickle.dumps(Pos[player])) # it will send data immediately once client is connected  

    while True:
        data = pickle.loads(conn.recv(2048))
        print("received :",data)

        Pos[player] = data 

        if not data :
            print("disconnected")
            break

        else:
            if player == 0 :
                reply =  Pos[1] 

            elif player == 1:
                reply = Pos[0]
                


        conn.sendall(pickle.dumps(reply))
       # conn.send(pickle.dumps(reply))

start()
c_player = 0
while True:
    
    conn, addr = s.accept()    #conn is object for sending ,receiving from or to the client 
    print(f"{c_player} joined") 
    start_new_thread(threaded_client,(c_player,conn,addr)) # new player 
    c_player += 1 # we must have c_player playerlist 



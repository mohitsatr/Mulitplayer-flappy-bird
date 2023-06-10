import pickle 
import socket

from _thread import start_new_thread


window_width = 400
window_height = 400


HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 6666  # Port to listen on (non-privileged ports are > 1023)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


def start():
    s.bind((HOST, PORT))
    s.listen()
    print("Server started waiting for new connection : ...")

# PlayersList = [
#     Player("Mohit"), Player("Raj")
# ]
initial_position = window_width-300,100

c_player = 0
Pos = [(initial_position),(initial_position)]
current_pos = [Pos[0],Pos[1]]

scores = [0,0]

def threaded_client(player,conn,addr):
    conn.send(pickle.dumps(Pos[player])) # it will send data immediately once client is connected  

    while True:
        data = pickle.loads(conn.recv(2048))
        print("received :",data)

        current_pos[player] = data["current_position"]

        if not data :
            print("disconnected")
            break


        else:
            if player == 0 :
                data["current_position"] =  current_pos[1]

            elif player == 1:
                data["current_position"] = current_pos[0]



        conn.send(pickle.dumps(data))

start()

while True:
    
    conn, addr = s.accept()    #conn is object for sending ,receiving from or to the client 
    print(f"{c_player} joined") 
    start_new_thread(threaded_client,(c_player,conn,addr)) # new player 
    c_player += 1 # we must have c_player playerlist 



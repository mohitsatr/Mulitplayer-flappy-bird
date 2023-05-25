import socket , pickle 

import numpy

class Network:
    def __init__(self) :
        self.HOST =  "localhost"  
        self.PORT = 5555
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = ((self.HOST,self.PORT))
    
        
    def connect(self):   
        try:
            self.client.connect(self.addr)

            data = self.client.recv(2048)
            if data:
                return pickle.loads(data)
            else:
                raise ConnectionError("No data received")
        except ConnectionError as e:
            print(f"Connection Error: {e}")
        except Exception as e:
            print(f"Error: {e}")



    def send(self,data):
        self.client.send(pickle.dumps(data))
        data = pickle.loads(self.client.recv(2048))
        return data
    





    

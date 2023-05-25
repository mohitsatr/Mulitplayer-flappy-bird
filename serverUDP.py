import socket

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set up the server address and port
server_address = ('localhost', 5555)  # Replace with your desired server address and port
server_socket.bind(server_address)

print("UDP server is running. Listening for incoming messages...")

while True:
    # Receive data from a client
    data, client_address = server_socket.recvfrom(1024)  # Adjust buffer size as needed

    # Process the received data (in this case, simply print it)
    print(f"Received data from {client_address}: {data.decode()}")

    # Send a response back to the client
    response = "Hello, client!"  # Customize your response message
    server_socket.sendto(response.encode(), client_address)

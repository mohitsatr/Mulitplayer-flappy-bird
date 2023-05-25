import socket

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set up the server address and port
server_address = ('localhost', 5555)  # Replace with the server address and port
message = "Hello, server!"  # Customize your message to the server

try:
    # Send data to the server
    client_socket.sendto(message.encode(), server_address)

    # Receive a response from the server
    response, server_address = client_socket.recvfrom(1024)  # Adjust buffer size as needed

    # Process the received response (in this case, simply print it)
    print(f"Received response from {server_address}: {response.decode()}")

finally:
    # Close the socket
    client_socket.close()

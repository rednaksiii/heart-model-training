import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(1)
conn, addr = server.accept()

while True:
    # Example: Send (x, y, z) values
    message = f"{cx},{cy},{depth}"
    conn.sendall(message.encode())

conn.close()

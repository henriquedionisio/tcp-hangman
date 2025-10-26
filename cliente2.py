import socket

HOST = "localhost"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024).decode()
        if not data:
            break

        print("[SERVIDOR]:", data)

        if data.startswith("STATE:"):
            letra = input("GUESS:Digite uma letra: ")
            msg = f"GUESS:{letra}"
            s.send(msg.encode())

        elif data.startswith("END:"):
            print("[FIM DO JOGO]:", data)
            break

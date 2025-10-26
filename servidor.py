import socket
import threading

HOST = "localhost"
PORT = 5000

clients = []
palavra_secreta = ""
estado_atual = ""
chances = 6
letras_usadas = set()
jogo_acabou = False


def atualizar_estado():
    global estado_atual
    estado = ""
    for letra in palavra_secreta:
        if letra in letras_usadas:
            estado += letra + " "
        else:
            estado += "_ "
    estado_atual = estado.strip()

def enviar_seguro(conn, msg):
    """Envia mensagem com proteção contra desconexão."""
    try:
        conn.send(msg.encode())
    except:
        print("[SERVIDOR] Erro ao enviar mensagem (cliente desconectado?)")

def handle_client(conn, addr, player_id):
    global palavra_secreta, chances, jogo_acabou

    print(f"[SERVIDOR] Jogador {player_id} conectado: {addr}")

    if player_id == 1:  # Jogador 1 define a palavra
        conn.send("SETWORD:Digite a palavra secreta:\n".encode())
        palavra_secreta = conn.recv(1024).decode().strip()
        print(f"[SERVIDOR] Palavra recebida: {palavra_secreta}")
        atualizar_estado()

        # Notifica jogador 2 que o jogo vai começar
        if len(clients) > 1:
            clients[1].send(f"STATE:{estado_atual} | Chances:{chances}\n".encode())

    elif player_id == 2:  # Jogador 2 tenta adivinhar
        while not jogo_acabou:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                if data.startswith("GUESS:"):
                    letra = data.split(":")[1]
                    print(f"[SERVIDOR] Jogador 2 tentou: {letra}")

                    if letra in letras_usadas:
                        conn.send("RESULT:repetida\n".encode())
                        continue

                    letras_usadas.add(letra)

                    if letra in palavra_secreta:
                        conn.send("RESULT:hit\n".encode())
                    else:
                        chances -= 1
                        conn.send("RESULT:miss\n".encode())

                    atualizar_estado()
                    conn.send(f"STATE:{estado_atual} | Chances:{chances}\n".encode())

                # Condições de fim
                if "_" not in estado_atual.replace(" ", ""):
                    enviar_seguro(conn, "END:win\n")
                    enviar_seguro(clients[0], "END:Jogador 2 venceu!\n")
                    jogo_acabou = True
                    print("[SERVIDOR] Jogo finalizado: Jogador 2 venceu!")
                    
                elif chances <= 0:
                    enviar_seguro(conn, f"END:lose:{palavra_secreta}\n")
                    enviar_seguro(clients[0], "END:Jogador 2 perdeu!\n")
                    jogo_acabou = True
                    print("[SERVIDOR] Jogo finalizado: Jogador 2 perdeu!")

            except:
                break
               
    conn.close()


def main():
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"[SERVIDOR] Aguardando jogadores em {HOST}:{PORT}...")

    player_id = 1
    while len(clients) < 2:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()
        player_id += 1


if __name__ == "__main__":
    main()
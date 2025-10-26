import socket

HOST = "localhost"
PORTA = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORTA))
        print("[CLIENTE 2] Conectado ao servidor.")

        s.send("JOGADOR:2".encode())

        while True:
            try:
                dados = s.recv(1024).decode()
                if not dados:
                    print("[CLIENTE 2] Conexão com o servidor perdida.")
                    break

                mensagens = dados.strip().split('\n')
                jogo_continua = True
                for msg in mensagens:
                    if not msg:
                        continue

                    print(f"[SERVIDOR] {msg}")

                    if msg.startswith("RESULT:REPEATED"):
                        print("\n[JOGO] Você já tentou essa letra. Tente outra.")
                    
                    elif msg.startswith("RESULT:HIT"):
                        print("\n[JOGO] Acertou!")

                    elif msg.startswith("RESULT:MISS"):
                        print("\n[JOGO] Errou!")

                    elif msg.startswith("END:"):
                        partes = msg.split(':')
                        resultado = partes[1]
                        palavra = partes[2]
                        if resultado == "WIN":
                            print(f"\n[FIM DE JOGO] Parabéns! Você venceu! A palavra era '{palavra}'.")
                        else: # LOSE
                            print(f"\n[FIM DE JOGO] Que pena! Você perdeu. A palavra era '{palavra}'.")
                        jogo_continua = False
                        break
                
                if not jogo_continua:
                    break

                # Se o jogo não acabou, sempre pede a próxima letra.
                # A presença de uma mensagem STATE na pilha de mensagens garante que temos o estado mais recente.
                if any(msg.startswith("STATE:") for msg in mensagens):
                    while True:
                        letra = input(" > Digite uma letra: ").strip()
                        if len(letra) == 1 and letra.isalpha():
                            s.send(f"GUESS:{letra}".encode())
                            break
                        else:
                            print("[CLIENTE 2] Entrada inválida. Por favor, digite apenas uma letra.")
            
            except ConnectionResetError:
                print("[CLIENTE 2] A conexão com o servidor foi redefinida.")
                break
            except Exception as e:
                print(f"[CLIENTE 2] Ocorreu um erro: {e}")
                break

if __name__ == "__main__":
    main()

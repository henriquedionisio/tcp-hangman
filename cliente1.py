import socket

HOST = "localhost"
PORTA = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORTA))
        print("[CLIENTE 1] Conectado ao servidor.")
        
        s.send("JOGADOR:1".encode())

        while True:
            try:
                dados = s.recv(1024).decode()
                if not dados:
                    print("[CLIENTE 1] Conexão com o servidor perdida.")
                    break

                for linha in dados.strip().split('\n'):
                    print(f"[SERVIDOR] {linha}")

                    if linha.startswith("SETWORD:"):
                        palavra = input(" > Digite a palavra secreta: ")
                        tema = input(" > Digite o tema: ")
                        s.send(f"{palavra},{tema}".encode())
                        print("\n[CLIENTE 1] Palavra e tema definidos. Aguardando o Jogador 2...")

                    elif linha.startswith("END:"):
                        partes = linha.split(':')
                        resultado = partes[1]
                        palavra = partes[2]
                        if resultado == "WIN":
                            print(f"\n[FIM DE JOGO] O Jogador 2 acertou a palavra '{palavra}'!")
                        else: # LOSE
                            print(f"\n[FIM DE JOGO] O Jogador 2 não conseguiu adivinhar a palavra '{palavra}'.")
                        break
                
                if "END:" in dados:
                    break

            except ConnectionResetError:
                print("[CLIENTE 1] A conexão com o servidor foi redefinida.")
                break
            except Exception as e:
                print(f"[CLIENTE 1] Ocorreu um erro: {e}")
                break

if __name__ == "__main__":
    main()

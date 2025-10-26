import socket
import threading
import time

HOST = "localhost"
PORTA = 5000

jogadores = {}
palavra_secreta = ""
tema = ""
estado_atual_palavra = ""
chances = 6
letras_usadas = set()
jogo_acabou = False
evento_reset = threading.Event()

def atualizar_estado_palavra():
    global estado_atual_palavra
    estado = ""
    for letra in palavra_secreta:
        if letra.lower() in letras_usadas:
            estado += letra + " "
        else:
            estado += "_ "
    estado_atual_palavra = estado.strip()

def enviar_mensagem(conexao, mensagem):
    try:
        conexao.send(mensagem.encode())
    except:
        print("[SERVIDOR] Erro ao enviar mensagem para um cliente desconectado.")

def gerenciar_cliente(conexao, endereco):
    global palavra_secreta, tema, chances, jogo_acabou, letras_usadas, jogadores

    id_jogador = None
    try:
        dados = conexao.recv(1024).decode().strip()
        if dados.startswith("JOGADOR:"):
            id_jogador = dados.split(":")[1]
            jogadores[id_jogador] = conexao
            print(f"[SERVIDOR] Jogador {id_jogador} conectado: {endereco}")
            
            if id_jogador == '1':
                enviar_mensagem(conexao, "INFO:Você é o Jogador 1. Aguarde o Jogador 2 se conectar.\n")
            else: # id_jogador == '2'
                enviar_mensagem(conexao, "INFO:Você é o Jogador 2.\n")
                # Notifica o Jogador 1 que o jogo pode começar
                if '1' in jogadores:
                    enviar_mensagem(jogadores['1'], "INFO:O Jogador 2 se conectou. O jogo vai começar!\n")
        else:
            print(f"[SERVIDOR] Conexão de {endereco} sem identificação. Fechando.")
            conexao.close()
            return
    except Exception as e:
        print(f"[SERVIDOR] Erro na identificação do jogador: {e}")
        conexao.close()
        return

    if id_jogador == '1': # Jogador 1 define a palavra
        enviar_mensagem(conexao, "SETWORD:Defina a palavra e o tema (formato: palavra,tema):\n")
        try:
            dados = conexao.recv(1024).decode().strip().lower()
            if not dados:
                raise ConnectionAbortedError("Jogador 1 desconectou antes de definir a palavra.")
            
            if "," in dados:
                palavra_secreta, tema = dados.split(",", 1)
                palavra_secreta = palavra_secreta.lower()
            else:
                palavra_secreta = dados.lower()
                tema = "Nenhum"
            
            print(f"[SERVIDOR] Palavra definida: '{palavra_secreta}', Tema: '{tema}'")
            atualizar_estado_palavra()

            if '2' in jogadores:
                enviar_mensagem(jogadores['2'], f"STATE:{estado_atual_palavra}|CHANCES:{chances}|TEMA:{tema}\n")
            
            # Mantém o jogador 1 ativo para receber o resultado do jogo
            while not jogo_acabou:
                time.sleep(0.5)

        except Exception as e:
            print(f"[SERVIDOR] Erro com o Jogador 1: {e}")
            jogo_acabou = True

    elif id_jogador == '2':
        enviar_mensagem(conexao, "INFO:Aguardando o Jogador 1 definir a palavra...\n")
        
        while not palavra_secreta and not jogo_acabou:
            time.sleep(0.5)

        while not jogo_acabou:
            try:
                dados = conexao.recv(1024).decode().strip()
                if not dados:
                    break

                if dados.startswith("GUESS:"):
                    try:
                        letra = dados.split(":", 1)[1].lower()
                        if not (len(letra) == 1 and letra.isalpha()):
                            enviar_mensagem(conexao, f"STATE:{estado_atual_palavra}|CHANCES:{chances}|TEMA:{tema}\n")
                            continue
                    except IndexError:
                        enviar_mensagem(conexao, f"STATE:{estado_atual_palavra}|CHANCES:{chances}|TEMA:{tema}\n")
                        continue
                    
                    print(f"[SERVIDOR] Jogador 2 chutou a letra: {letra}")

                    if letra in letras_usadas:
                        enviar_mensagem(conexao, "RESULT:REPEATED\n")
                        enviar_mensagem(conexao, f"STATE:{estado_atual_palavra}|CHANCES:{chances}|TEMA:{tema}\n")
                    else:
                        letras_usadas.add(letra)
                        if letra in palavra_secreta: # palavra_secreta já está em minúsculas
                            atualizar_estado_palavra()
                            enviar_mensagem(conexao, "RESULT:HIT\n")
                        else:
                            chances -= 1
                            enviar_mensagem(conexao, "RESULT:MISS\n")

                    atualizar_estado_palavra()

                    if "_" not in estado_atual_palavra:
                        msg_vitoria = f"END:WIN:{palavra_secreta}\n"
                        enviar_mensagem(conexao, msg_vitoria)
                        if '1' in jogadores: enviar_mensagem(jogadores['1'], msg_vitoria)
                        jogo_acabou = True
                        print("[SERVIDOR] Fim de jogo: Jogador 2 venceu!")
                    elif chances <= 0:
                        msg_derrota = f"END:LOSE:{palavra_secreta}\n"
                        enviar_mensagem(conexao, msg_derrota)
                        if '1' in jogadores: enviar_mensagem(jogadores['1'], msg_derrota)
                        jogo_acabou = True
                        print("[SERVIDOR] Fim de jogo: Jogador 2 perdeu!")
                    else:
                        enviar_mensagem(conexao, f"STATE:{estado_atual_palavra}|CHANCES:{chances}|TEMA:{tema}\n")

            except Exception as e:
                print(f"[SERVIDOR] Erro com o Jogador 2: {e}")
                break
    
    print(f"[SERVIDOR] Jogador {id_jogador} desconectado.")
    conexao.close()
    if id_jogador in jogadores:
        del jogadores[id_jogador]

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(2)
    print(f"[SERVIDOR] Aguardando jogadores em {HOST}:{PORTA}...")

    while True:
        global jogadores, palavra_secreta, tema, chances, letras_usadas, jogo_acabou, evento_reset, estado_atual_palavra
        jogadores = {}
        palavra_secreta = ""
        tema = ""
        estado_atual_palavra = ""
        chances = 6
        letras_usadas = set()
        jogo_acabou = False
        evento_reset.clear()
        
        print("\n[SERVIDOR] Nova rodada iniciada. Aguardando 2 jogadores...")
        
        threads = []
        for _ in range(2):
            conexao, endereco = servidor.accept()
            thread = threading.Thread(target=gerenciar_cliente, args=(conexao, endereco))
            thread.start()
            threads.append(thread)
        
        print("[SERVIDOR] Ambos os jogadores conectados. O jogo começou.")

        while not jogo_acabou:
            time.sleep(1)
        
        print("[SERVIDOR] Fim da rodada. Finalizando processos.")
        evento_reset.set()
        
        for thread in threads:
            thread.join()
        
        print("[SERVIDOR] Rodada finalizada. Reiniciando em 2 segundos.")
        time.sleep(2)

if __name__ == "__main__":
    main()

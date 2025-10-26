# TCP Hangman 🎮
Projeto desenvolvido como parte da disciplina **ACH2026 – Redes de Computadores da Universidade de São Paulo (EACH-USP)**.

## 🧩 Descrição
Aplicação em Python que implementa um **Jogo da Forca Multiplayer** utilizando **Sockets TCP e Threads**.
O sistema segue o modelo **Cliente-Servidor**, onde:

- **Servidor**: coordena a partida e gerencia as mensagens entre os jogadores.
- **Jogador 1**: escolhe a palavra secreta.
- **Jogador 2**: tenta adivinhar a palavra.

## ⚙️ Arquitetura
Comunicação via **TCP** (conexão confiável e ordenada).
Cada cliente é tratado em uma **thread** separada pelo servidor.
Protocolo próprio de mensagens. Principais: `SETWORD`, `STATE`, `GUESS`, `RESULT`, `END`.

## 💬 Protocolo de Comunicação
O protocolo define as seguintes mensagens para a comunicação entre cliente e servidor:

### Cliente → Servidor
- `JOGADOR:{1|2}`: Identifica o cliente como Jogador 1 ou 2.
- `SETWORD:{palavra},{tema}`: Jogador 1 define a palavra secreta e um tema.
- `GUESS:{letra}`: Jogador 2 envia um palpite.

### Servidor → Cliente
- `INFO:{mensagem}`: Envia informações gerais e de status.
- `STATE:{palavra_parcial}|CHANCES:{n}|TEMA:{tema}`: Envia o estado atualizado do jogo.
- `RESULT:{HIT|MISS|REPEATED}`: Informa o resultado de um palpite.
- `END:{WIN|LOSE}:{palavra_final}`: Anuncia o fim do jogo.

## 🚀 Execução
1. Abra **três terminais** no VSCode ou no sistema operacional.  
2. Execute na ordem:
   ```bash
   python servidor.py
   python cliente1.py
   python cliente2.py

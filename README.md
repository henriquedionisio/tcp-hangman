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
Protocolo próprio de mensagens (`SETWORD`, `STATE`, `GUESS`, `RESULT`, `END`).
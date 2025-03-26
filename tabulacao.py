import questionary, csv
from rich.console import Console
from rich.table import Table
from os import system
from time import sleep
from subprocess import run
from pathlib import Path
download_path = Path.home() / "GamTec"


def baixar_torrent(magnet_link,game):
    # Criar diretório se não existir
    pasta_destino = download_path / game
    pasta_destino.mkdir(parents=True, exist_ok=True)

    # Comando correto para iniciar o aria2c
    comando = [
    "aria2c",
    "--summary-interval=0",
    "--enable-rpc=false",
    "--rpc-listen-all",
    "--file-allocation=none",
    "--allow-overwrite=true",
    "--seed-time=0",
   "--dir", pasta_destino,
    magnet_link
]
    # Executa no PowerShell
    run(comando)
    sleep(5)
    clear_cmd()

# Limpa o Shell
def clear_cmd():
    system("cls")

# Retorna uma lista com cada atributo da tabela games.csv
def lista_jogos():
    jogos = []
    with open(r"Listas/games.csv", newline="") as file:
        leitor = csv.reader(file, delimiter=",")
        next(leitor)
        for linha in leitor:
            if linha:
                jogos.append((linha[0],linha[1],linha[2],linha[3]))
        return jogos


# Exibe a tabela de jogos para download
def print_tabela_jogos(jogos, lista_jogos, downloads: int):

    if downloads == 1:
        clear_cmd()
        nomes_jogos = [jogo[0] for jogo in lista_jogos]  # Lista apenas os nomes dos jogos

        #
        while True:
            para_baixar = questionary.checkbox(
                "Selecione os Jogos a serem instalados:",
                choices=nomes_jogos
            ).ask()
            clear_cmd()

            # Exibe as opções escolhidas de download
            if para_baixar:
                print(f"Jogos para baixar: ", ", ".join(para_baixar))
                print(f"\033[3;36mConfirma?\033[0;0m [Ss,Nn,Quit] <- [Bb] \033[1;31mGo Back\033[0m <--: ")
                confirma = input("> ")
                print("\n")

                if confirma.lower().strip() == "s":
                    for jogo_nome in para_baixar:
                        # Busca o jogo correspondente na lista completa
                        jogo_info = next((jogo for jogo in lista_jogos if jogo[0] == jogo_nome), None)

                        if jogo_info:
                            nome_jogo, tamanho, source, magnet_link = jogo_info  # Desempacota os valores corretamente
                            pasta_destino = download_path / nome_jogo
                            if magnet_link.startswith("http"):
                                run(["curl", magnet_link, "-o", f"{pasta_destino}.rar"])


                            else:
                                baixar_torrent(magnet_link,game=nome_jogo)  # Chama a função com os parâmetros corretos
                                if source.lower().strip() == "fitgirl":
                                    run(f'"{pasta_destino}\\{nome_jogo} [FitGirl Repack]\\setup.exe"',shell=True)
                                continue

                    break
                elif confirma.lower().strip() == "n":
                    continue
                elif confirma.lower().strip() == "b":
                    clear_cmd()
                    break
                elif confirma.lower().strip() == "quit":
                    clear_cmd()
                    exit()
                else:
                    clear_cmd()
                    print("Por favor, digite S/s, N/n ou Quit!")
                    sleep(1)
                    clear_cmd()
                    continue
            else:
                print("Nenhum jogo selecionado, por favor selecione algum!")

    # Exibe a tabela de jogos disponiveis
    elif downloads == 0:
        tabela = Table(title="Lista dos jogos")
        console = Console()
        tabela.add_column("Nome", style="cyan", justify="left")
        tabela.add_column("Tamanho", style="red", justify="center")
        tabela.add_column("Source", style="purple", justify="center")
        for jogo in jogos:
            tabela.add_row(*jogo[:3])
        console.print(tabela)

if __name__ == "__main__":
    while True:

        print("Listar Jogos [0], Tabela de Downloads [1], Sair [2]")
        input_inicial = str(input("> "))

        jogos = lista_jogos()
        if input_inicial == "0":
            clear_cmd()
            print_tabela_jogos(jogos=jogos, lista_jogos=jogos, downloads=0)
            continue
        elif input_inicial == "1":
            clear_cmd()
            print_tabela_jogos(jogos=jogos, lista_jogos=jogos, downloads=1)
            continue
        elif input_inicial == "2":
            clear_cmd()
            exit()
        else:
            print("Digite um valor valido!! ",end="")
            continue
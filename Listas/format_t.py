import csv


def reorganizar_csv(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, newline='', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile)

        # Definir a nova ordem das colunas
        campos = ['Nome', 'Tamanho', 'Source', 'Link']

        with open(arquivo_saida, mode='w', newline='', encoding='utf-8') as csv_saida:
            escritor = csv.DictWriter(csv_saida, fieldnames=campos)
            escritor.writeheader()

            for linha in leitor:
                escritor.writerow({
                    'Nome': linha['Nome'],
                    'Tamanho': linha['Tamanho'],
                    'Source': linha['Source'],
                    'Link': linha['Link']
                })


if __name__ == "__main__":
    entrada = "games-old.csv"  # Nome do arquivo de entrada
    saida = "games.csv"  # Nome do arquivo de saída
    reorganizar_csv(entrada, saida)
    print(f"Arquivo processado com sucesso! Salvo como {saida}")

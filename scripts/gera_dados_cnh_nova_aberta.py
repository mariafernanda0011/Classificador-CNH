import csv

def gerar_csv(frente_csv, verso_csv, saida_csv="csv/cnh_nova_dados_aberta.csv"):

    # Junta os dados da frente e do verso da CNH em um único CSV.
    dados_abertos = []

    # Abre os dois CSVs
    with open(frente_csv, newline='', encoding='utf-8') as f_frente, \
         open(verso_csv, newline='', encoding='utf-8') as f_verso:

        leitor_frente = csv.DictReader(f_frente)
        leitor_verso = csv.DictReader(f_verso)

        # Junta linha a linha
        for linha_frente, linha_verso in zip(leitor_frente, leitor_verso):
            combinado = {**linha_frente, **linha_verso}  # junta os dois dicionários
            dados_abertos.append(combinado)

        # Cabeçalho do CSV de saída (todos os campos da frente + verso)
        cabecalho = list(dados_abertos[0].keys())

    # Salva o CSV da CNH aberta
    with open(saida_csv, mode='w', newline='', encoding='utf-8') as f_saida:
        escritor = csv.DictWriter(f_saida, fieldnames=cabecalho)
        escritor.writeheader()
        for linha in dados_abertos:
            escritor.writerow(linha)

    print(f"{len(dados_abertos)} registros salvos em '{saida_csv}'.")


if __name__ == "__main__":
    frente_csv = "csv/cnh_nova_dados_frente.csv"
    verso_csv = "csv/cnh_nova_dados_verso.csv"
    gerar_csv(frente_csv, verso_csv)

import csv
from datetime import datetime, timedelta
from faker import Faker

def add_ten_years(dt):
    # Tenta adicionar 10 anos mantendo dia/mês; se der erro (ex.: 29/02), faz fallback.
    try:
        return dt.replace(year=dt.year + 10)
    except ValueError:
        return dt + timedelta(days=365 * 10 + 2)  # compensação aproximada

def gerar_csv(csv_frente, nome_arquivo_saida="cnh_nova_fake_verso.csv"):
    fake = Faker("pt_BR")

    count = 0 # A mesma quantidade de dados que tiver na frente terá no verso

    with open(csv_frente, mode="r", encoding="utf-8") as entrada, \
         open(nome_arquivo_saida, mode="w", newline="", encoding="utf-8") as saida:
        
        leitor = csv.DictReader(entrada)
        escritor = csv.writer(saida)
        escritor.writerow(["data_emissao", "validade", "local", "uf"])

        for linha in leitor:
            try:
                # Data de emissão é lida da frente
                data_emissao = datetime.strptime(linha["data_emissao"], "%d/%m/%Y")

                # Calcula validade (10 anos depois)
                validade = add_ten_years(data_emissao)

                # Gera local e UF aleatórios
                cidade = fake.city().upper()
                uf = fake.estado_sigla()

                escritor.writerow([
                    data_emissao.strftime("%d/%m/%Y"),
                    validade.strftime("%d/%m/%Y"),
                    cidade,
                    uf
                ])
                count += 1

            except Exception as e:
                print(f"Erro ao processar linha: {linha} -> {e}")

    print(f"Arquivo '{nome_arquivo_saida}' gerado com sucesso!")
    print(f"{count} CNHs fake salvas em '{nome_arquivo_saida}'")


if __name__ == "__main__":
    caminho_csv = 'cnh_nova_fake_frente.csv'
    gerar_csv(caminho_csv)

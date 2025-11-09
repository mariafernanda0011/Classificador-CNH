import csv
from faker import Faker

def gerar_csv(qtd_itens, nome_arquivo_saida="csv/cnh_nova_dados_verso.csv"):
    # Definindo o idioma
    fake = Faker("pt_BR")
    count = 0 

    estados = {
        "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
        "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
        "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
        "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
        "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"
    }

    with open(nome_arquivo_saida, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([
            "inf_completa", 
            "uf_extenso"
        ])

        for _ in range(qtd_itens):
            # Gera local e UF aleatórios
            cidade = fake.city().upper()
            uf_sigla = fake.estado_sigla()
            uf_extenso = estados[uf_sigla].upper() # Garante correspondência correta
            inf_completa = f"{cidade}, {uf_sigla}"
           
            # Escrevendo todos os campos no CSV
            escritor.writerow([
                inf_completa,
                uf_extenso
            ])

            count += 1

    print(f"{count} CNHs fake salvas em '{nome_arquivo_saida}'")

def contar_linhas_csv(arquivo_csv):
    # Conta quantas linhas (sem contar o cabeçalho) existem no CSV com os dados da frente.
    with open(arquivo_csv, newline='', encoding='utf-8') as f:
        leitor = csv.reader(f)
        next(leitor)  # Pula o cabeçalho
        return sum(1 for _ in leitor)

if __name__ == "__main__":
    arquivo_frente = "csv/cnh_nova_dados_frente.csv"
    qtd_itens = contar_linhas_csv(arquivo_frente)  # Conta quantos registros tem na frente
    gerar_csv(qtd_itens) # Gera a mesma quantidade para o verso

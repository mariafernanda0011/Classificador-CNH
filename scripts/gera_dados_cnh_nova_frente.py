import csv
import random
from faker import Faker
from datetime import datetime, timedelta

def gerar_csv(qtd_itens, nome_arquivo="cnh_nova_fake.csv"):
    # Definindo o idioma
    fake = Faker('pt_BR')
    categorias = ["ACC", "A", "A1", "B", "B1", "C", "C1", "D", "D1", "BE", "CE", "C1E", "DE", "D1E"]

    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)

        # Cabeçalho com labels da CNH nova (dados combinados já tratados)
        escritor.writerow([
            "nome_completo",
            "primeira_hab",
            "data_local_uf",
            "data_emissao",
            "validade",
            "identidade_emissor_uf",
            "cpf",
            "num_registro",
            "cat_hab",
            "nacionalidade",
            "filiacao_pai",
            "filiacao_mae"
        ])

        for _ in range(qtd_itens):
            # Nome completo
            nome = fake.name().upper()

            # Primeira habilitação (data)
            primeira_hab = fake.date_between(start_date='-30y', end_date='-18y').strftime("%d/%m/%Y")

            # Data, local e UF de nascimento (tudo junto)
            data_nasc = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%d/%m/%Y")
            cidade_nasc = fake.city().upper()
            uf_nasc = fake.estado_sigla()
            nascimento_completo = f"{data_nasc}, {cidade_nasc}, {uf_nasc}"

            # Data de emissão e validade
            data_emissao = fake.date_between(start_date='-5y', end_date='today').strftime("%d/%m/%Y")
            validade = (datetime.strptime(data_emissao, "%d/%m/%Y") + timedelta(days=random.randint(365*3, 365*10))).strftime("%d/%m/%Y")

            # Documento de identidade / órgão emissor / UF
            rg = f"{random.randint(10000000, 99999999)}"
            orgao = "SSP"
            uf_emissor = uf_nasc
            doc_completo = f"{uf_emissor}{rg} {orgao} {uf_emissor}"

            # CPF
            cpf = fake.cpf()

            # Número de registro
            registro_cnh = str(random.randint(10000000000, 99999999999))

            # Categoria de habilitação
            cat_hab = random.choice(categorias)

            # Nacionalidade
            nacionalidade = "BRASILEIRO(A)"

            # Filiação separada: pai e mãe
            filiacao_pai = fake.name_male().upper()
            filiacao_mae = fake.name_female().upper()

            # Escrevendo todos os campos no CSV
            escritor.writerow([
                nome,
                primeira_hab,
                nascimento_completo,
                data_emissao,
                validade,
                doc_completo,
                cpf,
                registro_cnh,
                cat_hab,
                nacionalidade,
                filiacao_pai,
                filiacao_mae
            ])

    print(f"{qtd_itens} CNHs fake salvas em '{nome_arquivo}'")


if __name__ == "__main__":
    qtd = int(input("Quantos registros deseja gerar? "))
    gerar_csv(qtd)

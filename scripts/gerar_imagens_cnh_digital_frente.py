import cv2
import csv
import json
import os
import sys

def gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida):
    tamanho_fonte = 0.3
    cor_padrao = (0, 0, 0) # preto
    cor_vermelha = (0, 0, 255)
    
    # Lê os dados do CSV
    dados_csv = []
    with open(csv_arquivo, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados_csv.append(linha)

    # Lê o JSON com posições de cada campo
    with open(json_arquivo, encoding='utf-8') as f:
        posicoes = json.load(f)

    # Garante que a quantidade não ultrapasse o total de registros disponíveis
    quantidade_imagens = min(quantidade_imagens, len(dados_csv))

    # Cada linha do CSV gera uma imagem (limitado pela quantidade escolhida)
    for id_item, dado in enumerate(dados_csv[:quantidade_imagens], start=1):
        imagem = cv2.imread(imagem_base)

        # Para cada campo do CSV, desenha o texto conforme a posição
        for campo, posicao in posicoes.items():
            if campo in dado:
                texto = str(dado[campo])

                # Define cor conforme o campo
                if campo in ["num_registro", "cat_hab", "validade"]:
                    cor = cor_vermelha
                else:
                    cor = cor_padrao

                cv2.putText(imagem, texto, tuple(posicao),
                            cv2.FONT_HERSHEY_SIMPLEX, tamanho_fonte, cor, 1, cv2.LINE_AA)

        # Salva a imagem
        nome_saida = os.path.join(pasta_saida, f"imagem_{id_item}.jpg")
        cv2.imwrite(nome_saida, imagem)

    print(f"{quantidade_imagens} imagens geradas na pasta '{pasta_saida}'")

def main():
    quantidade_imagens = 5
    imagem_base = "imagens/cnh_digital/CNH_frente/imagem_exemplo.jpg"
    csv_arquivo = "cnh_nova_fake.csv"
    json_arquivo = "posicoes.json"
    pasta_saida = "imagens/cnh_digital/CNH_frente"
    gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida)


if __name__ == "__main__":
    main()

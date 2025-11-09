import cv2
import csv
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np 

def gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida):

    tamanho_fonte = 10
    tamanho_fonte_maior = 16
    cor_padrao = (0, 0, 0) # preto
    cor_vermelha = (255, 0, 0)
    
    # Carregando a fonte
    font = ImageFont.truetype("font/MinionPro-Regular.otf", tamanho_fonte)
    font_grande = ImageFont.truetype("font/MinionPro-Regular.otf", tamanho_fonte_maior)


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
        # Carrega a imagem de exemplo/base
        imagem = cv2.imread(imagem_base)

        # Converte de OpenCV para PIL (BGR para RGB)
        imagem_pil = Image.fromarray(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(imagem_pil)

        # Para cada campo do CSV, desenha o texto conforme a posição
        for campo, posicao in posicoes.items():
            if campo in dado:
                texto = str(dado[campo])

                # Define cor conforme o campo
                if campo in ["num_registro", "cat_hab", "validade"]:
                    cor = cor_vermelha
                else:
                    cor = cor_padrao

                # Escolhe a fonte
                if campo in ["uf_extenso"]:  
                    fonte_usada = font_grande
                else:
                    fonte_usada = font
                
                # Desenhando as informações com a biblioteca Pil
                draw.text(
                    tuple(posicao),
                    texto,
                    font=fonte_usada,
                    fill=cor, # Pil usa RGB; OpenCV usa BGR
                    stroke_width=0.2,
                    stroke_fill=cor
                )

        # Converte Pil para OpenCV (RGB para BGR)
        imagem = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)

        # Salva a imagem
        nome_saida = os.path.join(pasta_saida, f"imagem_{id_item}.jpg")
        cv2.imwrite(nome_saida, imagem)

    print(f"{quantidade_imagens} imagens geradas na pasta '{pasta_saida}'")

def main():
    quantidade_imagens = 5

    # === Frente ===
    gerar_imagens(
        quantidade_imagens,
        imagem_base="imagens/cnh_digital/CNH_frente/imagem_exemplo.jpg",
        csv_arquivo="csv/cnh_nova_dados_frente.csv",
        json_arquivo="json/posicoes_cnh_nova_frente.json",
        pasta_saida="imagens/cnh_digital/CNH_frente"
    )

    # === Verso ===
    gerar_imagens(
        quantidade_imagens,
        imagem_base="imagens/cnh_digital/CNH_verso/imagem_exemplo2.jpg",
        csv_arquivo="csv/cnh_nova_dados_verso.csv",
        json_arquivo="json/posicoes_cnh_nova_verso.json",
        pasta_saida="imagens/cnh_digital/CNH_verso"
    )

    # === Aberta ===
    gerar_imagens(
        quantidade_imagens,
        imagem_base="imagens/cnh_digital/CNH_aberta/imagem_exemplo3.jpg",
        csv_arquivo="csv/cnh_nova_dados_aberta.csv",
        json_arquivo="json/posicoes_cnh_nova_aberta.json",
        pasta_saida="imagens/cnh_digital/CNH_aberta"
    )


if __name__ == "__main__":
    main()

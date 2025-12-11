import cv2
import os
import pandas as pd
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


from qr_feature_extractor import detectar_qr
from color_feature_extractor import get_colors_hsv, generate_color_features

print("O SCRIPT FOI INICIADO!")

def carregar_imagens(pasta_base):
    """
    Percorre todas as categorias e subpastas da pasta base
    e retorna uma lista de tuplas: (caminho_imagem, categoria, subpasta)
    """
    imagens = [] # Lista para armazenar os caminhos das imagens
    for categoria in os.listdir(pasta_base): # Para cada categoria
        pasta_categoria = os.path.join(pasta_base, categoria) # Caminho da categoria
        if not os.path.isdir(pasta_categoria): # Se não for pasta,
            continue # pula para a próxima
        # Para cada subpasta na categoria
        for subpasta in os.listdir(pasta_categoria):
            # Caminho da subpasta
            pasta_subpasta = os.path.join(pasta_categoria, subpasta)
            if not os.path.isdir(pasta_subpasta):
                continue
            # Para cada arquivo na subpasta
            for arquivo in os.listdir(pasta_subpasta):
                caminho_imagem = os.path.join(pasta_subpasta, arquivo) # Caminho completo
                # Verifica se é um arquivo de imagem válido
                if cv2.imread(caminho_imagem) is not None:
                    imagens.append((caminho_imagem, categoria, subpasta)) # Adiciona à lista
                else: # Arquivo inválido
                    print(f"Arquivo inválido: {caminho_imagem}")
    return imagens # Retorna a lista de imagens


def extrair_texto(img):
    """Extrai texto da imagem usando OCR."""
    return pytesseract.image_to_string(img)

def contar_palavras(texto):
    """Conta o número de palavras em um texto."""
    return len(texto.split())

def processar_imagem(caminho_imagem):
    """Processa uma única imagem e retorna um dicionário com os resultados."""
    img = cv2.imread(caminho_imagem)
    texto = extrair_texto(img)
    quantidade_palavras = contar_palavras(texto)
    
    return {
        "nome_arquivo": os.path.basename(caminho_imagem),
        "texto_extraido": texto.strip(),
        "quantidade_palavras": quantidade_palavras
    }


def obter_bag_palavras():
    """Retorna a lista de palavras de interesse para o modelo Bag of Words."""
    return [
        # termos comuns em CNH
        "transito",
        "carteira",
        "driver",
        "habilitacao",
        "nome",
        "validade",
        "identidade",
        "cat",
        "hab",
        "cpf",
        "assinatura",
        "portador",
        # cnh digital
        "transportes",
        'assinado',
        "digital",
        "estadual",
        # cnh fisica
        "infraestrutura",
        "emissor",
        "proibido",
        "plastificar"
    ]


def gerar_features_bag_palavras(df, bag_palavras):
    """Cria colunas de preseça para cada palavra do bag de palavras."""
    for palavra in bag_palavras: # Para cada palavra
        df[palavra] = df["texto_extraido"].apply( # Aplica função
            # Função lambda para verificar presença da palavra
            lambda texto: 1 if palavra.lower() in texto.lower() else 0 
        ) # Adiciona coluna ao DataFrame
    return df # Retorna DataFrame atualizado


def gerar_csv(resultados, nome_arquivo):
    """Gera um arquivo CSV com os resultados."""
    df = pd.DataFrame(resultados)
    df.to_csv(nome_arquivo, index=False, encoding="utf-8")
    print(f"CSV gerado: {nome_arquivo}")


def main():
    pasta_base = "imagens_transformadas"
    
    # Carrega todas as imagens, retornando tuplas (caminho, categoria, subpasta)
    imagens = carregar_imagens(pasta_base)

    # Agrupa imagens por categoria e subpasta
    grupos = {}
    for caminho, categoria, subpasta in imagens:
        chave = (categoria, subpasta)
        grupos.setdefault(chave, []).append(caminho)

    # Processa cada grupo (subpasta) e gera CSV separado usando gerar_csv()
    for (categoria, subpasta), lista_imagens in grupos.items():
        resultados = []


        for caminho_imagem in lista_imagens:
            print(f"\n Processando: {caminho_imagem}")
            print(" Lendo imagem...")
            
            # Features OCR
            print("Extraindo texto (OCR)...")
            resultado = processar_imagem(caminho_imagem)
            
            # Features QR code
            print("Detectando QR...")
            qr_feats = detectar_qr(caminho_imagem)
            resultado["qr_detectado"] = qr_feats
            print("QR OK")

            # Features de cor
            print("Extraindo cores HSV...")
            color_feats = generate_color_features(get_colors_hsv(caminho_imagem, num_colors=3))
            resultado.update(color_feats)
            print("Cores OK")

            # Adiciona categoria e subpasta
            resultado["categoria"] = categoria
            resultado["subpasta"] = subpasta

            resultados.append(resultado)

        # Converte para DataFrame
        df = pd.DataFrame(resultados)

        # Gera bag-of-words com a SUA função
        print("Gerando features Bag of Words...")
        df = gerar_features_bag_palavras(df, obter_bag_palavras())
        print("Bag of Words OK")
        
        print(" ===== OK, salvando dados...")
        nome_csv = f"features_{categoria}_{subpasta}.csv"
        gerar_csv(df.to_dict(orient="records"), nome_csv)

if __name__ == "__main__":
    main()

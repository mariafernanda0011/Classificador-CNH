import cv2
import albumentations as A
import os

# Pasta base de entrada
pasta_base = "imagens"

# Pasta base de saída
pasta_saida_base = "imagens_transformadas"
os.makedirs(pasta_saida_base, exist_ok=True)

# CNH Digital — variações discretas
transformacao_digital = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=0.05, contrast_limit=0.05, p=0.3), # leve ajuste de brilho/contraste
    A.MotionBlur(blur_limit=3, p=0.05), # leve desfoque de movimento
    A.CropAndPad(percent=(-0.01, 0.01), p=0.25), # leve corte e preenchimento
    A.ImageCompression(quality_range=(85, 95), p=0.5), # compressão da imagem
])

# CNH Física — variações realistas
transformacao_fisica = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.4), # 
    A.Rotate(limit=8, p=0.6), 
    A.MotionBlur(blur_limit=3, p=0.08), # desfoque de movimento
    A.GaussNoise(p=0.3), # ruído gaussiano
    A.CropAndPad(percent=(-0.08, 0.08), p=0.3), # leve corte e preenchimento
    A.HueSaturationValue(hue_shift_limit=5, sat_shift_limit=5, val_shift_limit=5, p=0.15), # ajuste de matiz/saturação/valor
    A.Perspective(scale=(0.01, 0.02), p=0.6), # distorção de perspectiva
    A.ImageCompression(quality_range=(75, 92), p=0.35), 
])


# Escolhe a transformação com base na categoria
def escolher_transformacao(nome_categoria):
    if "digital" in nome_categoria.lower():
        return transformacao_digital
    else:
        return transformacao_fisica

# Itera sobre cada categoria (subpasta)
for categoria in os.listdir(pasta_base):

    # Caminho completo da subpasta
    pasta_entrada = os.path.join(pasta_base, categoria)
    if not os.path.isdir(pasta_entrada):
        continue  # pula arquivos que não são pastas(arquivos soltos)

    # Escolhe a transformação apropriada
    transformacao = escolher_transformacao(categoria)

    # Subpastas: CNH_aberta, CNH_frente, CNH_verso
    for subpasta in os.listdir(pasta_entrada):
        pasta_subpasta = os.path.join(pasta_entrada, subpasta)
        if not os.path.isdir(pasta_subpasta):
            continue
    
        # Cria pasta de saída para a categoria
        pasta_saida = os.path.join(pasta_saida_base, categoria, subpasta)
        os.makedirs(pasta_saida, exist_ok=True)

        # Processa cada imagem na subpasta
        for arquivo in os.listdir(pasta_subpasta):

            caminho_arquivo = os.path.join(pasta_subpasta, arquivo)
            imagem = cv2.imread(caminho_arquivo)
            
            # Aplica a transformação
            imagem_aumentada = transformacao(image=imagem)["image"]
            
            # Salva a imagem transformada
            caminho_saida = os.path.join(pasta_saida, "aug_" + arquivo)
            cv2.imwrite(caminho_saida, imagem_aumentada)

        print(f"Processado: {categoria}/{subpasta}")
print("Todas as imagens foram processadas.")# Fim do script

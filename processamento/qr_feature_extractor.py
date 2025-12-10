import cv2

def detectar_qr(image_path):
    """Retorna 1 se a imagem contém QR Code, senão retorna 0."""

    # Carrega a imagem
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erro ao ler a imagem: {image_path}")
        return 0

    # OpenCV QRCode detector
    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(image)

    # Se detectou QR (mesmo vazio), points != None
    if points is not None:
        return 1
    else:
        return 0
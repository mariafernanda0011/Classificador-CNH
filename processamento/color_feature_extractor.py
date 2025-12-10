import cv2
import numpy as np

def get_colors_hsv(image_path, num_colors=3):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro ao ler imagem: {image_path}")
        return []

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape((-1, 3))
    pixels = np.float32(pixels)

    # critério de parada
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.1)

    _, labels, centers = cv2.kmeans(
        data=pixels,
        K=num_colors,
        bestLabels=None,
        criteria=criteria,
        attempts=10,
        flags=cv2.KMEANS_RANDOM_CENTERS
    )

    hsv_list = []
    for center in centers:
        rgb = np.uint8([[center]])
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0][0]

        hsv_list.append({
            "h": int(hsv[0]),
            "s": int(hsv[1]),
            "v": int(hsv[2]),
        })

    return hsv_list


def generate_color_features(hsv_list):
    features = {}
    for i, hsv in enumerate(hsv_list):
        features[f"color{i+1}_h"] = hsv["h"]
        features[f"color{i+1}_s"] = hsv["s"]
        features[f"color{i+1}_v"] = hsv["v"]
    return features

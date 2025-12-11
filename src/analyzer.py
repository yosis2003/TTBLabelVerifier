import cv2
import numpy as np
from paddleocr import PaddleOCR

# Initialize PaddleOCR once (this loads the model)
ocr = PaddleOCR(
    use_angle_cls=True,      # handles rotated text
    lang='en',               # English
)

def preprocess_image(path):
    """Preprocess the image to help OCR on real-world photos."""
    img = cv2.imread(path)

    # Convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize if image is huge (helps stability)
    max_dim = 1600
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    # Light denoising (helps noisy backgrounds)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    return img

def extract_text(img_path):
    img = preprocess_image(img_path)

    # Run OCR
    result = ocr.ocr(img)

    for res in result:
        res.print()

    lines = []
    for block in result:
        for text_info in block:
            text = text_info[1][0]     # Raw recognized text
            lines.append(text)

    return lines


if __name__ == "__main__":
    image_path = "/home/yosis/Desktop/secondsample.jpeg"  # <--- replace with your path

    text_lines = extract_text(image_path)

    print("\n--- OCR OUTPUT ---\n")
    for line in text_lines:
        print(line)

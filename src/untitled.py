import os
import math
!pip install --quiet google-cloud-vision
from collections import Counter
from google.cloud import vision
import re

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='vision_key.json'
WORD = re.compile(r"\w+")

def detect_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # for non-dense text 
    # response = client.text_detection(image=image)
    # for dense text
    response = client.document_text_detection(image=image)
    texts = response.text_annotations
    ocr_text = []

    for text in texts:
        ocr_text.append(f"\r\n{text.description}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return ocr_text


from PIL import Image, ImageDraw
image_path = ''

directory = "/home/yosis/Downloads/Total-Text/Test"
for root, directories, filenames in os.walk(directory):
    for name in filenames:
        if name.endswith(".jpg"):
            image_path = root + "/" + name
            print(root + "/" + name)
            text = detect_text(root + "/" + name)
            
            image
            for line in text:
                print(line)
# for name in os.listdir(directory):
#     file_path = os.path.join(directory, name)
#     if os.path.isfile(file_path):
#         with open(file_path, 'r') as f:
#             text = detect_text(file_path)



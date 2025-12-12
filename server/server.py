import os
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import vision

# -------------------------------------------------
# Flask Setup
# -------------------------------------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'

# -------------------------------------------------
# OCR
# -------------------------------------------------
def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations

    ocr_lines = []
    for item in texts:
        ocr_lines.append(item.description.strip())

    if response.error.message:
        raise Exception(response.error.message)

    return ocr_lines

# -------------------------------------------------
# Matching Logic
# -------------------------------------------------

def find_abv(ocr_text):
    """
    Extracts alcohol percentage from OCR text.
    Looks for patterns like '5%', '12.5%', etc.
    """
    pattern = r"(\d{1,2}(?:\.\d+)?\s?%)"
    matches = re.findall(pattern, " ".join(ocr_text))
    if matches:
        # return numeric form e.g. "12.5%" -> 12.5
        return matches[0].replace(" ", "")
    return None


def find_volume(ocr_text):
    """
    Detects and normalizes volume from OCR text.
    Converts everything to mL.
    """

    text = " ".join(ocr_text).lower()

    # --- Detect milliliters (ml) ---
    ml_match = re.findall(r"(\d+)\s?m[l]", text)
    if ml_match:
        return f"{ml_match[0]} ml"

    # --- Detect centiliters (cl) ---
    cl_match = re.findall(r"(\d+(?:\.\d+)?)\s?c[l]", text)
    if cl_match:
        cl_value = float(cl_match[0])
        ml = int(round(cl_value * 10))  # 1 cL = 10 mL
        return f"{ml} ml"

    # --- Detect liters (l) ---
    l_match = re.findall(r"(\d+(?:\.\d+)?)\s?l", text)
    if l_match:
        liters = float(l_match[0])
        ml = int(round(liters * 1000))
        return f"{ml} ml"

    # --- Detect fluid ounces (fl oz / oz) ---
    # 1 fl oz = 29.5735 mL
    oz_match = re.findall(r"(\d+(?:\.\d+)?)\s?(?:fl oz|oz)", text)
    if oz_match:
        ounces = float(oz_match[0])
        ml = int(round(ounces * 29.5735))
        return f"{ml} ml"

    return None




def fuzzy_match(keyword, text):
    """
    Basic fuzzy match by checking if keyword exists in any OCR line
    (case-insensitive, partial match).
    """
    keyword = keyword.lower().strip()
    for line in text:
        if keyword in line.lower():
            return line
    return None


def compare_values(label_value, detected_value, field_name):
    """
    Helper to construct a standard comparison object.
    """
    if detected_value is None:
        return {
            "match": False,
            "value_found": None,
            "message": f"{field_name} not found in label."
        }

    # Normalize numeric comparisons
    if field_name == "ABV":
        try:
            label_val_num = float(label_value)
            detected_num = float(detected_value.replace("%", ""))
        except:
            return {
                "match": False,
                "value_found": detected_value,
                "message": "Unable to compare ABV values."
            }

        if abs(label_val_num - detected_num) < 0.01:
            return {
                "match": True,
                "value_found": detected_value,
                "message": "ABV matches label."
            }
        else:
            return {
                "match": False,
                "value_found": detected_value,
                "message": f"ABV does not match. Detected {detected_value}."
            }

    # String comparison for brand + type
    if label_value.lower() in detected_value.lower():
        return {
            "match": True,
            "value_found": detected_value,
            "message": f"{field_name} found in label."
        }

    return {
        "match": False,
        "value_found": detected_value,
        "message": f"{field_name} does not match. Found '{detected_value}'."
    }


# -------------------------------------------------
# API Endpoint
# -------------------------------------------------

@app.route("/api/upload", methods=['POST'])
def upload_image():

    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Form data
    brand_name = request.form.get("brandName", "")
    product_type = request.form.get("productType", "")
    abv = request.form.get("abv", "")
    net_contents = request.form.get("netContents", "")

    # OCR
    try:
        ocr_output = detect_text(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # ----- Perform comparisons -----

    detected_abv = find_abv(ocr_output)
    detected_volume = find_volume(ocr_output)
    detected_brand = fuzzy_match(brand_name, ocr_output)
    detected_type = fuzzy_match(product_type, ocr_output)

    abv_compare = compare_values(abv, detected_abv, "ABV")
    volume_compare = compare_values(net_contents, detected_volume, "Volume")
    brand_compare = compare_values(brand_name, detected_brand, "Brand Name")
    type_compare = compare_values(product_type, detected_type, "Alcohol Type")

    # ----- Final JSON Response -----

    return jsonify({
        "message": "File processed",
        "ocr_output": ocr_output,
        "comparisons": {
            "abv": abv_compare,
            "volume": volume_compare,
            "brand": brand_compare,
            "type": type_compare
        }
    })


@app.route("/api/home", methods=['GET'])
def home():
    return jsonify({"message": "Hello World"})


if __name__ == "__main__":
    app.run(debug=True, port=8080)

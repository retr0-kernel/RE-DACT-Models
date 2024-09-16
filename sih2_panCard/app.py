import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
import os

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust for your system

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return gray

def extract_text_and_boxes(image):
    preprocessed = preprocess_image(image)
    data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DICT)
    return data

def redact_info(image, data, patterns):
    n_boxes = len(data['level'])
    regions_to_redact = []

    for i in range(n_boxes):
        text = data['text'][i]
        if any(re.search(pattern, text) for pattern in patterns.values()):
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            regions_to_redact.append((x, y, w, h))
    
    for (x, y, w, h) in regions_to_redact:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)
    
    return image

def save_redacted_image(image, output_path):
    cv2.imwrite(output_path, image)

def process_pan_card_image(file_path):
    image = cv2.imread(file_path)
    data = extract_text_and_boxes(image)
    
    patterns = {
        "Name": r"^[A-Z\s]+$",  
        "Father's Name": r"^[A-Z\s]+$",  
        "Date of Birth": r"\d{2}/\d{2}/\d{4}", 
        "PAN Number": r"[A-Z]{5}\d{4}[A-Z]{1}", 
    }
    
    redacted_image = redact_info(image, data, patterns)
    

    output_file = f"redacted_{os.path.basename(file_path)}"
    output_path = os.path.join('output', output_file)
    
    if not os.path.exists('output'):
        os.makedirs('output')
    
    save_redacted_image(redacted_image, output_path)
    return output_path

def process_input_folder():
    input_folder = 'input'
    output_folder = 'output'

    if not os.path.exists(input_folder):
        print(f"Input folder '{input_folder}' does not exist. Please create it and place images inside.")
        return
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_folder, filename)
            print(f"Processing file: {input_path}")
            output_file = process_pan_card_image(input_path)
            print(f"Redacted file saved as: {output_file}")

if __name__ == "__main__":
    process_input_folder()


import cv2
import pytesseract
import argparse
import re
from scipy import ndimage
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# To detect orientation and perform rotation
def rotate(image, center = None, scale = 1.0):
    angle=int(re.search('(?<=Rotate: )\d+', pytesseract.image_to_osd(image)).group(0))
    (h, w) = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    rotated = ndimage.rotate(image, float(angle) * -1)
    return rotated

# To perform preprocessing before OCR
def preprocessing(image):
    w, h = image.shape[0],image.shape[1]
    if w < h:
        image = rotate(image)
    resized_image = cv2.resize(image, None, fx=1.75, fy=1.75, interpolation=cv2.INTER_LINEAR)
    grey_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.medianBlur(grey_image, 3)
    thres_image = cv2.adaptiveThreshold(blur_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,13,7)

    return thres_image, resized_image

# To perform OCR and mask first 8 digits
def aadhar_mask_and_ocr(thres_image, resized_image):
    d = pytesseract.image_to_data(thres_image, output_type=pytesseract.Output.DICT)
    number_pattern = r"(?<!\d)\d{4}(?!\d)"
    n_boxes = len(d['text'])
    c, temp, UID = 0, [], []
    final_image = resized_image.copy()
    
    for i in range(n_boxes):
        if int(d['conf'][i]) > 20:
            if re.match(number_pattern, d['text'][i]):
                if c < 2:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    final_image = cv2.rectangle(final_image, (x, y), (x + w, y + h), (255, 255, 255), -1)
                    temp.append(d['text'][i])
                    c += 1
                elif c >= 2 and d['text'][i] in temp:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    final_image = cv2.rectangle(final_image, (x, y), (x + w, y + h), (255, 255, 255), -1)
                elif c == 2:
                    UID = temp + [d['text'][i]]
                    c += 1
    
    final_image = cv2.resize(final_image, None, fx=0.33, fy=0.33)
    return final_image, UID



# Command-line argument
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
    help = "Path to the image to be scanned")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

thres_image, resized_image = preprocessing(image)
masked_image, UID = aadhar_mask_and_ocr(thres_image, resized_image)

print("Original image size:", image.shape)
print("Resized image size:", resized_image.shape)
print('Masked digits in given image. Displaying...')
cv2.imshow('mask' + args["image"], masked_image)

# To save ouput, uncomment below line
cv2.imwrite('mask' + args["image"], masked_image)
print('UID' + ' : ' + ' '.join(UID))
print('Press q over output window to close')
cv2.waitKey(0)


# aadhar-mask-ocr

Python code to perform Masking on First 8 digits of Aadhar and also perform OCR to return UID
Packages used: Tesseract, OpenCV, Scipy

Usage:
`python aadhar_mask_ocr.py --image images/img1.jpeg`

Output:\
`Masked digits in given image. Displaying...`\
![alt text](https://github.com/Vignesh-Desmond/aadhar-mask-ocr/blob/main/masked_images/maskimg3.png)\
`UID : 3429 2099 3643`\
`Press q over output window to close`


Unmasked Image             | Masked Image 
:-------------------------:|:-------------------------:
![](https://github.com/Vignesh-Desmond/aadhar-mask-ocr/blob/main/images/img1.jpeg)  |  ![](https://github.com/Vignesh-Desmond/aadhar-mask-ocr/blob/main/masked_images/maskimg1.jpeg)
![](https://github.com/Vignesh-Desmond/aadhar-mask-ocr/blob/main/images/img2.jpeg)  |  ![](https://github.com/Vignesh-Desmond/aadhar-mask-ocr/blob/main/masked_images/maskimg2.jpeg)

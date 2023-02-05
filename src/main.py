# Your code lives here, Good luck!
import json
import matplotlib.pyplot as plt
import os
import re
from jiwer import cer, wer
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageEnhance


def preprocessImage(image_path, new_img_path):
    # Convert image grayscale
    image = Image.open(image_path).convert('L')
    # Improve image contrast and sharpness
    improved_image = ImageEnhance.Contrast(image).enhance(1.5)
    improved_image = ImageEnhance.Sharpness(image).enhance(1.5)
    # Check if new path folders exist  
    folder = '/'.join(new_img_path.split('/')[:-1])
    # Create the new path folders if does exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Save the improved image in the new path
    improved_image.save(new_img_path)

def getTextFromImage(OCR, image_path):
    text = []
    # Detect and recognize text using OCR
    result = OCR.ocr(image_path, cls=True)
    for res in result[0]:
        text.append(res[1])
    return text 

def filterArabicText(text_list):
    arabic_text = []
    for i in text_list:
    	# Only filter Arabic text
        if re.findall(r'^[a-zA-Z0-9.?,!-]+', i[0]) == []:
        	# Filter Arabic text with a presicion of 75%.
            if i[1] >= 0.75:
                arabic_text.append(i[0])
    return arabic_text

def filterEnglishText(text_list):
    english_text = []
    for i in text_list:
    	# Filter English text with a presicion of 80%.
        if i[1] >= 0.8:
            english_text.append(i[0])
    return english_text

def extractTextFromImage(images_path_list):
    text = {}
    # Loop on each provided image path 
    for image_path in images_path_list:
    	# Extract filename from the path
        image_name = image_path.split('/')[-1]
        # Generate path for preprocessed image
        new_img_path = './input/preprocessed_images/' + image_name
        # Check the existence of the image
        if os.path.exists(image_path):
        	# Perform preprocessing effect on the image
            preprocessImage(image_path, new_img_path)
            # Extract English and Arabic text from the image
            english_result = getTextFromImage(english_ocr, new_img_path)
            arabic_result = getTextFromImage(arabic_ocr, new_img_path)
            # Save text result in dict type variable
            text[image_name] = filterEnglishText(english_result) + filterArabicText(arabic_result)
        else :
            print("File " + image_path + " does not exist.")
    return text

def evaluate_results(actual_output_file, true_output_file):
	# Check if the output files exist
    if os.path.exists(actual_output_file) and os.path.exists(true_output_file):
    	# Load the two files
        actual_output = json.load(open(actual_output_file, 'r'))
        true_output = json.load(open(true_output_file, 'r'))
        # Calculate the CER and WER scores for each text image and display the two scores   
        for i in actual_output:
            cer_error = cer(' '.join(actual_output[i]), ' '.join(true_output[i]))
            wer_error = wer(' '.join(actual_output[i]), ' '.join(true_output[i]))
            print(i + " :\n\t- CER : " + str(cer_error) + "\n\t- WER : " + str(wer_error))
    else :
        print("File " + actual_output_file + ", " + true_output_file + " or both do not exist")

# Initialize English OCR and Arabic OCRs
english_ocr = PaddleOCR(use_angle_cls=True, lang='en')
arabic_ocr = PaddleOCR(use_angle_cls=True, lang='ar')
# Provided image paths
images_path = [ 
                './input/input_1.png',
                './input/input_2.png',
                './input/input_3.png',
                './input/input_4.png',
                './input/input_5.png'
                ]
# Initialize the output file path
output_file = '.output/output.json'
# Get the output folder path
output_folder = '/'.join(output_file.split('/')[:-1])
# Checks if the path of the output folder exists and creates the necessary folders if it does not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Get the text from the provided image paths
result = extractTextFromImage(images_path)
# Store the result in JSON file
with open(output_file, "w") as f:
        json.dump(result, f, indent=4, ensure_ascii = False)
# Evaluate the text results with the actual text 
evaluate_results("./output/output.json", "./output/true_output.json")
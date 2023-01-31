import matplotlib.pyplot as plt
import os
from easyocr import Reader
import keras_ocr
import json
import cv2
from pathlib import Path
import jiwer 

# first we going to use sone libraries for OCR (tesseract, easyocr , kerasocr between these three kerasocr gave better results compared to the others 

def ocr_rec(inputs, output, plt=False):
    """
    This function performs keras OCR recognition on all images in the specified folder and writes the recognized text to a JSON file.
    Optionally, it can also display the image with the recognized text drawn on top using matplotlib.

    Parameters:
    - inputs (str): Path to the folder containing the images or the image to be processed
    - output (str): Path to the output JSON file
    - plt (bool): Whether or not to display the images with the recognized text drawn on top using matplotlib. Defaults to False.
    """
    pipeline = keras_ocr.pipeline.Pipeline()

    if Path(inputs).is_dir():
        input_images = [file for file in Path(inputs).iterdir() if file.is_file()]
    else:
        input_images = [Path(inputs)]

    images = [keras_ocr.tools.read(str(img)) for img in input_images]
    prediction_groups = pipeline.recognize(images)

    data = {Path(image).name: [prediction[0] for prediction in predictions] for image, predictions in zip(input_images, prediction_groups)}

    for image_name, recognized_text in data.items():
        print(f"{image_name}: {recognized_text}")

    with open(output, "w") as f:
        json.dump(data, f, indent=4)

    if(plt):
        for i, (image, prediction_group) in enumerate(zip(images, prediction_groups)):
            keras_ocr.tools.drawAnnotations(image, prediction_group)
            plt.imshow(image)
            plt.show() 


# ocr_rec('.\input',".\output\output.json")

# with visualization :
# ocr_rec('.\input',"output.json",True)


#the results was decent for the first part, some reasons is due to different styles, vertical texts and low quality pictures 
# so in this section we replace some pictures with better quality ones (1,3,4,5) for the input_5 we only take the rotated version to analyse the vertical text

# ocr_rec('.\input2',".\output\output2.json")

#it surely gave better results but keep lacking some words and  mispelling some


def arabic_OCR(inputs, output_folder):
    """
    Perform Arabic Optical Character Recognition (OCR) on the images in the input folder.
    Bounding boxes are drawn around the recognized text in the output images, which are saved in the output folder.
    The OCR results are also saved in a JSON file in the output folder.
    
    Parameters:
    inputs (str): The path to the input folder containing the images or the path to the image.
    output_folder (str): The path to the output folder where the output images and JSON file will be saved.
    
    """
    reader = Reader(['ar'])
    results = {}
    
    if os.path.isfile(inputs):
        file_name = Path(inputs).name
        words = [result[1] for result in reader.readtext(cv2.imread(inputs))]
        results[file_name] = words
        print(f"{file_name}: {words}")
    else:
        for image_path in Path(inputs).iterdir():
            if image_path.is_file():
                file_name = image_path.name
                words = [result[1] for result in reader.readtext(cv2.imread(str(image_path)))]
                results[file_name] = words
                print(f"{file_name}: {words}")
    
    output_file = Path(output_folder) / 'arabicOCR_results.json'
    with output_file.open(mode='w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)



#arabic_OCR('./input', './output/arabicOCR_output/')


# JIWER  Validation for english (the result of output was stored in tst.json to simplify the comparison)

with open("src/actual_text.json", 'r') as f:
    actual_text = json.load(f)

with open('src/tst.json', 'r') as f:
    predicted_text = json.load(f)


def jiwer_val(actual_text, predicted_text):
    for actual_img in actual_text:
        for predicted_img in predicted_text:
            if actual_img == predicted_img:
                wer = jiwer.wer(actual_text[actual_img], predicted_text[predicted_img])
                cer = jiwer.cer(actual_text[actual_img], predicted_text[predicted_img])
                print("CER for image", actual_img, ":", cer)
                print("WER for image", actual_img, ":", wer)
                

jiwer_val(actual_text, predicted_text)

# Final results :  the arabicOCR gave also some decent results but can't judge with giving less words than non-arabic (english) 

# Solution to improve is to train our own model using some state-of-art modles of Scene Text Recognition such as PARSeq, CDistNet, S-GTR












from ArabicOcr import arabicocr
import cv2
import os
import json
import matplotlib.pyplot as plt



def arabic_OCR(input_folder, output_folder):
    """
    Perform Arabic Optical Character Recognition (OCR) on the images in the input folder.
    Bounding boxes are drawn around the recognized text in the output images, which are saved in the output folder.
    The OCR results are also saved in a JSON file in the output folder.
    
    Parameters:
    input_folder (str): The path to the input folder containing the images.
    output_folder (str): The path to the output folder where the output images and JSON file will be saved.
    
    """
    # Get the list of input images
    input_images = [os.path.join(input_folder, file_name) for file_name in os.listdir(input_folder)]
    
    # Dictionary to store the OCR results for each image
    results = {}
    
    # Perform OCR on each image in the input folder
    for image_path in input_images:
        # Get the file name without the extension
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Create the path to the output image
        out_image = os.path.join(output_folder, file_name +'_bounding_box'+ '.jpg')
        
        # Perform OCR on the current image
        results2 = arabicocr.arabic_ocr(image_path, out_image)
        
        # Get the recognized words
        words=[]
        for i in range(len(results2)): 
            word=results2[i][1]
            words.append(word)
        
        # Store the OCR results for the current image
        results[file_name] =({'image_name': file_name, 'words': words})
    
    # Write the OCR results to a JSON file
    with open(os.path.join(output_folder, 'arabicOCR_results.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)



arabic_OCR('./input/', './output/arabicOCR_output/')


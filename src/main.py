import matplotlib.pyplot as plt
import os
import keras_ocr
import json
import cv2

# first we going to use sone libraries for OCR (tesseract, easyocr , kerasocr between these three kerasocr gave better results compared to the others 
# P.S : we do not consider arabic characters

def ocr_rec(folder_path, output, plt=False):
    """
    This function performs keras OCR recognition on all images in the specified folder and writes the recognized text to a JSON file.
    Optionally, it can also display the image with the recognized text drawn on top using matplotlib.

    Parameters:
    - folder_path (str): Path to the folder containing the images to be processed
    - output (str): Path to the output JSON file
    - plt (bool): Whether or not to display the images with the recognized text drawn on top using matplotlib. Defaults to False.
    """
       # Initialize the OCR pipeline
    pipeline = keras_ocr.pipeline.Pipeline()

    # Get the list of input images
    input_images = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]

    # Read the images
    images = [
        keras_ocr.tools.read(img) for img in input_images
    ]

    # Perform OCR on the images
    prediction_groups = pipeline.recognize(images)

    # Initialize an empty dictionary to store the data
    data = {}

    # Iterate through the prediction groups and input images
    for image, predictions in zip(input_images, prediction_groups):
        # Get the image name
        image_name = os.path.basename(image)
        image_name, _ = os.path.splitext(image_name)
        
        # Get the recognized text for the image
        recognized_text = [prediction[0] for prediction in predictions]
        
        # Add the image data to the dictionary
        data[image_name] = {
            "image_name": image_name,
            "words": recognized_text
        }

    # Save the data to the json file
    with open(output, "w") as f:
        json.dump(data, f, indent=4)

    # If plt flag is true
    if(plt):
        # Iterate through the images and prediction groups
        for i, (image, prediction_group) in enumerate(zip(images, prediction_groups)):
            # Draw the annotations (bounding boxes and recognized text) on the image
            keras_ocr.tools.drawAnnotations(image, prediction_group)
            # Display the image
            plt.imshow(image)
            plt.show()


ocr_rec('.\input',".\output\output.json")

# with visualization :
# ocr_rec('.\input',"output.json",True)


#the results was decent for the first part, some reasons is due to different styles, vertical texts and low quality pictures 
# so in this section we replace some pictures with better quality ones (1,3,4,5) for the input_5 we only take the rotated version to analyse the vertical text

ocr_rec('.\input2',".\output\output2.json")

#it surely gave better results but keep lacking some words and  mispelling some


def compare_word_sets(predicted_words_file, actual_words_file="src/actual_text.json"):
    """
    This function compares the sets of words in two dictionaries and returns the common words.
    Parameters:
    actual_words_file (str): Path to the file containing the actual words.
    predicted_words_file (str): Path to the file containing the predicted words.

    """
    # Load the actual words dictionary
    with open(actual_words_file, "r") as f:
        actual_words_dict = json.load(f)

    # Load the predicted words dictionary
    with open(predicted_words_file, "r") as f:
        predicted_words_dict = json.load(f)

    # Iterate over the actual words dictionary
    for image_name, actual_words in actual_words_dict.items():
        actual_words_set = set(actual_words["words"])
        predicted_words_set = set(predicted_words_dict[image_name]["words"])
        
        # Compare the sets
        common_words = actual_words_set & predicted_words_set
        print(f"For image '{image_name}', common words are: {common_words}")


#for first section with the original images
compare_word_sets('./output/output.json')

#for first section with different images
compare_word_sets('./output/output2.json')

# We see how for input2 images there is more common words



#for sack of simplicity the arabic OCR will be in another file (arabicOCR.py)

# Final results :  the arabicOCR gave also some decent results but can't judge with giving less words than non-arabic (english) 

# Solution to improve is to train our own model using some state-of-art modles of Scene Text Recognition such as PARSeq, CDistNet, S-GTR










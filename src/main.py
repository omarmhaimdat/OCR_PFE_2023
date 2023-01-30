### packages importing
import os
import cv2
import numpy as np
import json
import jiwer
import pytesseract
import time


### input images reading
def read_img_from_source():
  images_array = []
  absolute_input_path = os.path.abspath("../input")
  input_images_nouns = os.listdir(absolute_input_path)
  input_images_nouns.remove(".ipynb_checkpoints")
  for input_images_noun in input_images_nouns:
     img = cv2.imread(absolute_input_path+"/"+input_images_noun, cv2.IMREAD_COLOR)
     img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
     images_array = images_array + [img]
  images_array = np.array(images_array)
  return images_array,input_images_nouns

### apply preprocessing operations on brute images
def preprocess_images(images_array):
  processed_arrays = []
  for img in images_array:
    # resizing image to (500,500)
    resized_img = cv2.resize(img,(500,500), interpolation = cv2.INTER_AREA)
    norm_img = np.zeros((resized_img.shape[0], resized_img.shape[1]))
    # normalizing pixels value between 0 and 1
    normalized_img = cv2.normalize(resized_img, norm_img, 0, 255, cv2.NORM_MINMAX)
    processed_arrays += [normalized_img]
  return processed_arrays


### pytesseract image text conversion
def extract_text_content(processed_arrays):
  images_predicted_text_content = []
  for processed_img in processed_arrays:
    images_predicted_text_content += [pytesseract.image_to_string(processed_img)]
  return images_predicted_text_content

### post-process output text produced by pytesseract
def text_post_processing(images_predicted_text_content,input_files_names):
    # python dictionary that stores image text content to be written in output
    dictionary = {}
    for i in range(0,len(images_predicted_text_content)):
    ## text post-processing
       splitted_content = images_predicted_text_content[i].split("\n")
       # eliminate all space strings, empty strings, End_of_file sign
       content = list(filter(("").__ne__, splitted_content))
       content = list(filter((" ").__ne__, content))
       content = list(filter(("  ").__ne__, content))
       content = list(filter(("\f").__ne__, content))
       dictionary[input_files_names[i]] = content
    return dictionary

start_time = time.time()
### main workflow
images_array,input_files_nouns = read_img_from_source()
processed_arrays = preprocess_images(images_array)
images_predicted_text_content = extract_text_content(processed_arrays)
output_dict = text_post_processing(images_predicted_text_content,input_files_nouns)
print("--- Total processing time : %s seconds ---" % (time.time() - start_time))

### output Json file
# Serializing json
json_object = json.dumps(output_dict, indent=4)
# Writing to output.json
absolute_output_path = os.path.abspath("../output")
with open(absolute_output_path+"output.json", "w") as outfile:
    outfile.write(json_object)


### Character Error Rate (CER) and Word Error Rate (WER) metrics computation
images_ground_truth_text = ["shopkees.com\nJAN 26TH TO FEB 2HD\nSale starts at 12.00 pm (GST)\n\nCOUPON CODE\nWNTR\nUse coupon for additional discount\nMEGA\nWINTER\nSALE\nUPTO\n60 OFF",
                            "Attijariwafa bank\n2023\nAttijari Entreprise\nattijarientreprise.com\nattijariCIB.com",
                            "YES, LET'S PLAY\nALL NEW\nYARIS\nDISPONIBLE EN BOITE AUTOMATIQUE\nORIGINAL\nHYBRID\nA PARTIR DE\n900DHMOIS\nVRAI\nCREDIT\nGRATUIT", 
                            "NITRO\n12  we",
                            "CRYSTAL PLAZA\nUP TO 8\nYEARS INSTALLMENTS\n15% DOWN PAYMENT\nMEMAAR\nALMORSHEDY"]

wer_error = jiwer.wer(images_ground_truth_text,images_predicted_text_content)
cer_error = jiwer.cer(images_ground_truth_text,images_predicted_text_content)
print("Word Error Rate = ",wer_error)
print("Character Error Rate = ",cer_error)
 
 
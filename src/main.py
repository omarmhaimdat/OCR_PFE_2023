# Your code lives here, Good luck!
# Your code lives here, Good luck!
#!pip install keras-ocr

import keras_ocr
import json


def getImageFromPath(image_path):
    # Read image
    image = keras_ocr.tools.read(image_path)

    return image


def getWordsList(prediction_groups):
    # Get only the predected word
    detections = []
    for prediction in prediction_groups[0]:
        detections.append(prediction[0])

    return detections


def storeResult(output_file, data):
    # Save the result data in json file
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


def main():
    # Initialize pipeline
    pipeline = keras_ocr.pipeline.Pipeline()

    # Providing the images path
    paths = ['./input/input_1.png',
             './input/input_2.png',
             './input/input_3.png',
             './input/input_4.png',
             './input/input_5.png']

    result = {}

    for path in paths:
        # Get the image
        img = getImageFromPath(path)
        # Get the predicted words from the image 
        prediction_groups = pipeline.recognize([img])
        result[path.split('/')[-1]] = getWordsList(prediction_groups)

    # Storing the results
    storeResult('./output/output.json', result)


if __name__ == "__main__":
    main()
# Your code lives here, Good luck!

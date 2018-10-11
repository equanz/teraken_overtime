from keras import models
from PIL import Image
import numpy as np
import os, glob

# CONST VAL
DATASET_DIR = os.getenv('PREDICT_DIR')
LABEL_NAME = ['not_north', 'north']

def load_model():
    global model
    with open(os.getenv('DUMP_DIR') + "/north_model_cnn.json", 'r') as f:
        model = models.model_from_json(f.read())
        model.model.load_weights(os.getenv('DUMP_DIR') + "/north_params_cnn.hdf5")
        model.compile(loss="mse", optimizer='sgd', metrics=["acc"]) # compile model


def make_npimage(image_file):
    RESIZE_VAL = 150 # resized by 150
    image = Image.open(image_file)
    image = image.convert("RGB")
    image = image.resize((RESIZE_VAL, RESIZE_VAL))
    return np.asarray(image) # return image array

def predict(X_predict):
    global model

    feature = model.predict(X_predict)
    return feature

def main():
    load_model() # load model
    image_dir = DATASET_DIR + "/" + LABEL_NAME[1]
    image_files = glob.glob(image_dir + "/*.jpg")

    for image_file in image_files:
        image_path = str(image_file)
        x = make_npimage(image_path)
        x = np.expand_dims(x, axis=0)

        feature = predict(x)
        if feature[0, 0] != 1:
            print(image_path + ": " + str(feature[0, 0]))

if __name__ == "__main__":
    main()


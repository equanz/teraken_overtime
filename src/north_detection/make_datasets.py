from PIL import Image
import tempfile, glob
import random, math
import numpy as np

# CONST VAL
DUMP_DIR = os.getenv('HOME') + "/teraken_overtime_dump"
DATASET_DIR = DUMP_DIR + "/labeled"
LABEL_NAME = ['not_north', 'north']

def make_npdatasets(image_files):
    X = []
    y = []
    for label, image_file in image_files:
        # append to X, y
        X.append(make_npimage(image_file))
        y.append(label)
    return np.array(X), np.array(y)

def make_npimage(image_file):
    RESIZE_VAL = 150 # resized by 150
    image = Image.open(image_file)
    image = image.convert("RGB")
    image = image.resize((RESIZE_VAL, RESIZE_VAL))
    return np.asarray(image) # return image array

def main():
    datasets_array = []

    for i, label in enumerate(LABEL_NAME):
        image_dir = DATASET_DIR + "/" + label
        image_files = glob.glob(image_dir + "/*.jpg")
        for image_file in image_files:
            datasets_array.append((i, image_file))

    # shuffle datasets
    random.shuffle(datasets_array)
    train_size = math.floor(len(datasets_array) * 0.6)
    val_size = math.floor(len(datasets_array) * 0.2)
    X_train, y_train = make_npdatasets(datasets_array[0:train_size])
    X_val, y_val = make_npdatasets(datasets_array[train_size:train_size + val_size])
    X_test, y_test = make_npdatasets(datasets_array[train_size + val_size:])

    # save dataset array
    xy = (X_train, X_val, X_test, y_train, y_val, y_test)
    np.save(DUMP_DIR + "/north_datasets.npy", xy)

if __name__ == "__main__":
    main()

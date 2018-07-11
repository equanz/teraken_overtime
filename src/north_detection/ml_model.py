from keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import os

# CONST VAL
DATASET_DIR = os.getenv('DATASET_DIR')
LABEL_NAME = ['not_north', 'north']

def create_model():
    global model, model_stack
    RESIZE_VAL = 150 # resized by 150
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(RESIZE_VAL, RESIZE_VAL, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation="relu"))
    model.add(layers.Dense(1, activation="sigmoid"))

    model.summary() # show summary

    model.compile(loss="binary_crossentropy", optimizer='sgd', metrics=["acc"]) # compile model
    return model

def train_model(datasets_path):
    global model, model_stack
    X_train, X_test, y_train, y_test = np.load(datasets_path)
    X_train = X_train.astype("float") / 255
    X_test  = X_test.astype("float")  / 255
    model_stack = model.fit(X_train, y_train, epochs=10, batch_size=6, validation_data=(X_test, y_test))

def show_history():
    global model, model_stack
    acc = model_stack.history['acc']
    val_acc = model_stack.history['val_acc']
    loss = model_stack.history['loss']
    val_loss = model_stack.history['val_loss']

    # plot learning curve
    x = range(len(acc))
    plt.style.use('dark_background')
    plt.plot(x, acc, label="train acc")
    plt.plot(x, val_acc, label="test acc")
    plt.title("accuracy")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

    plt.plot(x, loss, label='train loss')
    plt.plot(x, val_loss, label='test loss')
    plt.title('cost')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

def main():
    datasets_path = os.getenv('DUMP_DIR') + "/north_datasets.npy"
    create_model()

    train_model(datasets_path) # training model
    show_history()

    # save model
    model_string = model.model.to_json()
    open(os.getenv('DUMP_DIR') + "/north_predict.json", 'w').write(model_string)

    # save parameter
    model.model.save_weights(os.getenv('DUMP_DIR') + "/north_predict.hdf5")

if __name__ == "__main__":
    main()


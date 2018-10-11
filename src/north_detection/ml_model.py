from keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import os

# CONST VAL
DUMP_DIR = os.getenv('HOME') + "/teraken_overtime_dump"
DATASET_DIR = os.getenv('HOME') + "/teraken_overtime_dump/labeled"
LABEL_NAME = ['not_north', 'north']

%matplotlib inline

def create_model():
    RESIZE_VAL = 150 # resized by 150
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(RESIZE_VAL, RESIZE_VAL, 3))) # conv layer
    model.add(layers.MaxPooling2D((2, 2))) # pooling layer
    model.add(layers.Conv2D(64, (3, 3), activation="relu")) # conv layer
    model.add(layers.MaxPooling2D((2, 2))) # pooling layer
    model.add(layers.Conv2D(128, (3, 3), activation="relu")) # conv layer
    model.add(layers.MaxPooling2D((2, 2))) # pooling layer
    model.add(layers.Conv2D(128, (3, 3), activation="relu")) # conv layer
    model.add(layers.MaxPooling2D((2, 2))) # pooling layer
    model.add(layers.Flatten()) # flatten layer
    model.add(layers.Dense(512, activation="relu")) # fully connect layer 1
    model.add(layers.Dense(1, activation="sigmoid")) # fully connect layer 2 (output)

    model.summary() # show summary

    model.compile(loss="binary_crossentropy", optimizer='sgd', metrics=["acc"]) # compile model
    return model

def train_model(model, datasets_path):
    X_train, X_val, X_test, y_train, y_val, y_test = np.load(datasets_path)
    X_train = X_train.astype("float") / 255
    X_val = X_val.astype("float") / 255
    model_stack = model.fit(X_train, y_train, epochs=10, batch_size=6, validation_data=(X_val, y_val))
    return model_stack

def show_history(model_stack):
    acc = model_stack.history['acc']
    val_acc = model_stack.history['val_acc']
    loss = model_stack.history['loss']
    val_loss = model_stack.history['val_loss']

    # plot learning curve
    epoch = range(len(acc))
    plt.style.use('dark_background')
    plt.plot(epoch, acc, label="train acc")
    plt.plot(epoch, val_acc, label="val acc")
    plt.title("accuracy")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

    plt.plot(epoch, loss, label='train loss')
    plt.plot(epoch, val_loss, label='val loss')
    plt.title('loss')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    
def evaluate_data(model, datasets_path):
    X_train, X_val, X_test, y_train, y_val, y_test = np.load(datasets_path)
    X_test  = X_test.astype("float")  / 255
    eval_stack = model.evaluate(x=X_test, y=y_test)
    return eval_stack

def main():
    datasets_path = DUMP_DIR + "/north_datasets.npy"
    model = create_model()

    model_stack = train_model(model, datasets_path) # training model
    show_history(model_stack)

    # save model
    model_string = model.to_json()
    open(DUMP_DIR + "/north_model_cnn.json", 'w').write(model_string)

    # save parameter
    model.save_weights(DUMP_DIR + "/north_params_cnn.hdf5")

if __name__ == "__main__":
    main()

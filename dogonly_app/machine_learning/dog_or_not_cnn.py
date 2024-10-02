import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense, BatchNormalization
from keras.utils import np_utils
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflow as tf
import numpy as np
import os

parent_directory = "./photos/"
categories = ['dog', 'another']
num_classes = len(categories)

image_size = 50

class TestCallback(tf.keras.callbacks.Callback):
    def __init__(self, X, Y):
        super().__init__()
        self.X = X
        self.Y = Y
        self.best_accuracy = 0

    def on_epoch_end(self, epoch, logs=None):
        scores = self.model.evaluate(self.X, self.Y, verbose=1)
        test_accuracy = scores[1]
        print('Test Loss: ', scores[0])
        print('Test Accuracy: ', test_accuracy)
        if test_accuracy > self.best_accuracy:
            self.best_accuracy = test_accuracy
            self.model.save('./dog_or_not_cnn.h5')
            print(f'New best model saved with accuracy: {test_accuracy:.4f}')
        else:
            print(f'Model not improved; current best accuracy: {self.best_accuracy:.4f}')

def model_train(X_train, Y_train, X_test, Y_test):
    model = Sequential()
    model.add(Conv2D(32, (3,3), padding='same', input_shape=X_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3,3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    opt = Adam(learning_rate=0.0001, decay=1e-6)

    model.compile(loss='categorical_crossentropy',
                  optimizer=opt, metrics=['accuracy'])

    callback = keras.callbacks.EarlyStopping(monitor='loss', patience=3)

    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=96, epochs=100, callbacks=[callback, TestCallback(X_test, Y_test)])

    return model

def main():
    X_train, X_test, Y_train, Y_test = np.load("./dog_or_not.npy", allow_pickle=True)
    X_train = X_train.astype("float32") / 255.0
    X_test = X_test.astype("float32") / 255.0
    Y_train = np_utils.to_categorical(Y_train, num_classes)
    Y_test = np_utils.to_categorical(Y_test, num_classes)

    model = model_train(X_train, Y_train, X_test, Y_test)

if __name__ == '__main__':
    main()

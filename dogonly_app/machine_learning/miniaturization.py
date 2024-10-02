import tensorflow as tf

model = tf.keras.models.load_model('dog_or_not_cnn.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('dog_or_not.tflite', 'wb') as f:
    f.write(tflite_model)
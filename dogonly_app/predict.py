import os
import numpy as np
from PIL import Image
from django.conf import settings

categories = ['dog', 'another']
image_size = 50

USE_TFLITE_RUNTIME = os.getenv('DJANGO_ENV') in ['production', 'docker']

if USE_TFLITE_RUNTIME:
    import tflite_runtime.interpreter as tflite
    model_path = settings.TFLITE_MODEL_PATH
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
else:
    # ローカル環境
    import tensorflow as tf
    model_path = settings.MODEL_PATH
    model = tf.keras.models.load_model(model_path)



def preprocess_image(image):
    image = Image.open(image).convert('RGB')
    image = image.resize((image_size, image_size))
    data = np.asarray(image) / 255.0
    return np.expand_dims(data, axis=0).astype(np.float32)

def predict(image):
    X = preprocess_image(image)

    USE_TFLITE_RUNTIME = os.getenv('DJANGO_ENV') == 'production'
    
    if USE_TFLITE_RUNTIME:
        interpreter.set_tensor(input_details[0]['index'], X)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
    else:
        output_data = model.predict(X)
    
    predicted = np.argmax(output_data)
    return categories[predicted]

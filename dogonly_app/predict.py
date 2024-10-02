import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
from django.conf import settings
import os

categories = ['dog', 'another']
image_size = 50

interpreter = tflite.Interpreter(model_path=settings.MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_image(image):
    image = Image.open(image).convert('RGB')
    image = image.resize((image_size, image_size))
    data = np.asarray(image) / 255.0
    return np.expand_dims(data, axis=0).astype(np.float32)

def predict(image):
    X = preprocess_image(image)
    
    interpreter.set_tensor(input_details[0]['index'], X)
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted = np.argmax(output_data)
    
    return categories[predicted]

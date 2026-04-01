import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os 
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'Model', 'model.h5')
model = load_model(MODEL_PATH)

class_names = ['Acne and Rosacea Photos',
 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions',
 'Atopic Dermatitis Photos',
 'Bullous Disease Photos',
 'Cellulitis Impetigo and other Bacterial Infections',
 'Eczema Photos',
 'Exanthems and Drug Eruptions',
 'Hair Loss Photos Alopecia and other Hair Diseases',
 'Herpes HPV and other STDs Photos',
 'Light Diseases and Disorders of Pigmentation',
 'Lupus and other Connective Tissue diseases',
 'Melanoma Skin Cancer Nevi and Moles',
 'Nail Fungus and other Nail Disease',
 'Poison Ivy Photos and other Contact Dermatitis',
 'Psoriasis pictures Lichen Planus and related diseases',
 'Scabies Lyme Disease and other Infestations and Bites',
 'Seborrheic Keratoses and other Benign Tumors',
 'Systemic Disease',
 'Tinea Ringworm Candidiasis and other Fungal Infections',
 'Urticaria Hives',
 'Vascular Tumors',
 'Vasculitis Photos',
 'Warts Molluscum and other Viral Infections']

def predict_image(image_path):
    print("INSIDE PREDICT IMAGE")

    # Convert InMemoryUploadedFile to numpy array
    file_bytes = np.asarray(bytearray(image_path.read()), dtype=np.uint8)
    test_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Convert to RGB
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    # Resize to match model input
    test_img = cv2.resize(test_img, (256, 256))

    # Normalize pixel values to [0, 1]
    test_img = test_img / 255.0

    # Reshape to (1, 256, 256, 3) → batch of 1
    test_input = test_img.reshape((1, 256, 256, 3))

    # Predict
    prediction = model.predict(test_input)[0]

    # Get class with highest probability
    predicted_index = np.argmax(prediction)
    confidence = prediction[predicted_index]

    # Map index to class name
    predicted_class = class_names[predicted_index]

    return predicted_class, confidence

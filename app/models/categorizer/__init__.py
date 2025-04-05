import joblib
import numpy as np

def load_model_and_vectorizer():
    model = joblib.load("models/text_classifier1.pkl")
    vectorizer = joblib.load("models/product_vectorizer1.pkl")
    return model, vectorizer

MODEL, VECTORIZER = load_model_and_vectorizer()
CLASSES = ['Аксессуары', 'Аренда', 'Еда', 'Зарплата', 'Одежда и обувь', 'Разное', 'Транспорт']

def predict(product_name: str):
    vector = VECTORIZER.transform([product_name])
    
    proba = MODEL.predict_proba(vector)[0]

    best_index = np.argmax(proba)
    predicted_class = MODEL.classes_[best_index]
    confidence = proba[best_index] * 100

    return CLASSES[predicted_class]

import joblib
import numpy as np

def load_model_and_vectorizer():
    model = joblib.load("models/text_classifier1.pkl")
    vectorizer = joblib.load("models/product_vectorizer1.pkl")
    return model, vectorizer

def predict_category(product_name, model, vectorizer):
    vector = vectorizer.transform([product_name])
    
    proba = model.predict_proba(vector)[0]

    best_index = np.argmax(proba)
    predicted_class = model.classes_[best_index]
    confidence = proba[best_index] * 100

    return predicted_class, confidence

def main():
    print("=== Предсказание категории по названию продукта ===")
    model, vectorizer = load_model_and_vectorizer()

    while True:
        product_name = input("\nВведите название продукта (или 'выход' для завершения): ").strip()
        if product_name.lower() in {"выход", "exit"}:
            print("Выход из программы.")
            break
        
        predicted_class, confidence = predict_category(product_name, model, vectorizer)
        classes = ['Аксессуары', 'Аренда', 'Еда', 'Зарплата', 'Одежда и обувь', 'Разное', 'Транспорт']
        
        print(f"Категория: {classes[predicted_class]} (уверенность: {confidence:.2f}%)")

if __name__ == "__main__":
    main()

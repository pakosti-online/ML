from joblib import load

# Загружаем обученную модель и векторизатор
model = load("models/text_classifier1.pkl")
vectorizer = load("models/product_vectorizer1.pkl")

# Получаем важность признаков
importances = model.get_feature_importance()

feature_names = vectorizer.get_feature_names_out()

import matplotlib.pyplot as plt
import numpy as np

indices = np.argsort(importances)[::-1]
top_n = 30

plt.figure(figsize=(12, 6))
plt.title("Top TF-IDF Feature Importances")
plt.bar(range(top_n), importances[indices[:top_n]], align="center")
plt.xticks(range(top_n), [feature_names[i] for i in indices[:top_n]], rotation=90)
plt.tight_layout()

plt.savefig("feature_importances1.png")
print("График сохранён как feature_importances1.png")


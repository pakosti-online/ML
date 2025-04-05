import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("/home/fotuneb/ML/dataset.csv")

df = df.dropna(subset=["Категория", "Продукт"])

X_text = df["Продукт"]
y = df["Категория"]

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4), max_features=3000, min_df=5, max_df=0.7)
X_vec = vectorizer.fit_transform(X_text)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print(label_encoder.classes_)
print(set(y_encoded))

X_train, X_test, y_train, y_test = train_test_split(X_vec, y_encoded, test_size=0.2, random_state=42)

class_weights = {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3}

model = CatBoostClassifier(
    iterations=2000,
    depth=8,
    learning_rate=0.01,
    loss_function='MultiClass',
    verbose=50,
    random_seed=42,
    class_weights=class_weights
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, "models/product_vectorizer1.pkl")
joblib.dump(vectorizer, "models/product_vectorizer1.pkl")

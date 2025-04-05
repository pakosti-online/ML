import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor, Pool
import joblib
import optuna


def prepare_data(csv_path: str):
    df = pd.read_csv(csv_path)

    df['Изменение баланса'] = pd.to_numeric(df['Изменение баланса'], errors='coerce')
    df['Баланс'] = pd.to_numeric(df['Баланс'], errors='coerce')
    df['День покупки'] = pd.to_numeric(df['День покупки'], errors='coerce')
    df['Месяц покупки'] = pd.to_numeric(df['Месяц покупки'], errors='coerce')
    df = df.dropna()

    # Целевая переменная — баланс следующей транзакции
    df['target'] = df['Баланс'].shift(-1)
    df = df.dropna()

    X = df[['Изменение баланса', 'Баланс', 'День покупки', 'Месяц покупки', 'Категория']]
    y = df['target']

    cat_features = ['Категория']
    return X, y, cat_features


def objective(trial, X_train, y_train, X_val, y_val, cat_features):
    params = {
        "iterations": trial.suggest_int("iterations", 100, 1000),
        "depth": trial.suggest_int("depth", 4, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1e-3, 10.0, log=True),
        "random_strength": trial.suggest_float("random_strength", 1e-3, 10.0, log=True),
        "loss_function": "MAE",
        "verbose": 0,
        "random_seed": 42
    }

    model = CatBoostRegressor(**params)
    model.fit(X_train, y_train, cat_features=cat_features)

    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    return mae


def train_model(csv_path: str, model_path="catboost_model.pkl"):
    X, y, cat_features = prepare_data(csv_path)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    print("🔍 Оптимизация гиперпараметров с помощью Optuna...")
    study = optuna.create_study(direction="minimize")
    study.optimize(lambda trial: objective(trial, X_train, y_train, X_val, y_val, cat_features), n_trials=30)

    print(f"✅ Лучшие параметры: {study.best_params}")

    best_model = CatBoostRegressor(**study.best_params, loss_function="MAE", verbose=0)
    best_model.fit(X_train, y_train, cat_features=cat_features)

    # Метрики
    def evaluate(model, X, y, dataset_name=""):
        preds = model.predict(X)
        mae = mean_absolute_error(y, preds)
        rmse = np.sqrt(mean_squared_error(y, preds))
        r2 = r2_score(y, preds)
        print(f"📊 Метрики для {dataset_name}:")
        print(f"  MAE:  {mae:.2f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  R²:   {r2:.4f}\n")

    evaluate(best_model, X_train, y_train, "Train")
    evaluate(best_model, X_val, y_val, "Test")

    joblib.dump((best_model, cat_features), model_path)
    print(f"💾 Модель сохранена в: {model_path}")


# Запуск
train_model("/home/fotuneb/ML/dataset.csv")  # Укажи путь к своему CSV

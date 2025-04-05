import pandas as pd
import pickle
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from sklearn.preprocessing import LabelEncoder

# 1. Загрузка данных из CSV
data = pd.read_csv('test.csv')

# 2. Преобразование категориальных данных
encoder = LabelEncoder()
data['category_id'] = encoder.fit_transform(data['category_id'])

# 3. Подготовка данных для обучения
X = data[['category_id', 'balance', 'delta']]
y = data['balance']  # Целевая переменная - баланс

# 4. Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Обучение модели
model = CatBoostRegressor(iterations=1000, depth=6, learning_rate=0.1, loss_function='RMSE', cat_features=[0])  # Признак category_id категориальный

# Обучаем модель
model.fit(X_train, y_train)

# 6. Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# 7. Метрики
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Выводим метрики
print(f'Mean Absolute Error (MAE): {mae}')
print(f'Mean Squared Error (MSE): {mse}')
print(f'Root Mean Squared Error (RMSE): {rmse}')
print(f'R-squared (R²): {r2}')

# 8. Сохранение модели и encoder
model.save_model('financial_model.cb')
with open('encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)



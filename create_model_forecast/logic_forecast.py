from datetime import datetime, timedelta

# Пример данных
data = [
    {"id": 1, "product_name": "string", "date_created": "2025-04-05T10:45:07.742121Z", "category": "Разное", "balance": 0, "delta": 0, "user_id": 2},
    {"id": 2, "product_name": "string", "date_created": "2025-04-05T10:45:54.249902Z", "category": "Разное", "balance": 0, "delta": 0, "user_id": 2},
    {"id": 3, "product_name": "string", "date_created": "2025-04-05T10:46:17.371957Z", "category": "Разное", "balance": 0, "delta": 0, "user_id": 2},
    {"id": 13, "product_name": "string", "date_created": "2025-04-05T10:49:39.829105Z", "category": "Разное", "balance": 1000, "delta": -1000, "user_id": 2},
    {"id": 14, "product_name": "string", "date_created": "2025-04-05T10:49:43.246949Z", "category": "Разное", "balance": 2000, "delta": -1000, "user_id": 2},
    {"id": 17, "product_name": "string", "date_created": "2025-04-05T10:52:08.061758Z", "category": "Зарплата", "balance": 1000, "delta": 1000, "user_id": 2}
]

# Функция для расчета текущего состояния
def calculate_current_state(data):
    income = 0  # Доходы
    expenses = 0  # Расходы
    balance = 0  # Начальный баланс

    # Проходим по данным и суммируем доходы и расходы
    for entry in data:
        if entry['category'] == 'Зарплата':
            income += entry['delta']  # Добавляем доход
        else:
            expenses += abs(entry['delta'])  # Добавляем расходы для всех категорий, кроме "Зарплата"

    # Возвращаем сумму доходов, расходов и текущий баланс
    balance = income - expenses
    return balance, income, expenses

# Функция для прогнозирования состояния на N дней
def predict_balance_on_days(data, N):
    current_balance, total_income, total_expenses = calculate_current_state(data)
    
    # Прогноз на N дней: предполагаем, что доходы и расходы останутся постоянными
    daily_income = total_income / len([entry for entry in data if entry['category'] == 'Зарплата'])
    daily_expenses = total_expenses / len([entry for entry in data if entry['category'] != 'Зарплата'])
    
    projected_balance = current_balance
    
    # Прогнозируем изменения баланса на N дней
    for _ in range(N):
        projected_balance += daily_income - daily_expenses
    
    return projected_balance

# Прогнозируем баланс на 30 дней вперед
days_ahead = 3
projected_balance = predict_balance_on_days(data, days_ahead)
print(f"Прогнозируемое финансовое состояние пользователя через {days_ahead} дней: {projected_balance}")

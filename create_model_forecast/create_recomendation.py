import json
from collections import defaultdict
from dateutil.parser import parse as parse_date

# === Утилиты ===

def week_key(date_str):
    dt = parse_date(date_str)
    return f"{dt.year}-W{dt.isocalendar().week}"

# === Рекомендация: топ расходов ===

def generate_recommendations(transactions):
    category_spend = defaultdict(float)
    category_counts = defaultdict(int)

    for t in transactions:
        delta = t["delta"]
        cat = t["category"]
        if delta < 0:
            category_spend[cat] += -delta
            category_counts[cat] += 1

    recommendations = []

    if category_spend:
        top_category = max(category_spend, key=category_spend.get)
        spent = category_spend[top_category]
        count = category_counts[top_category]
        recommendations.append(
            f"Вы тратите больше всего на категорию '{top_category}': {spent:.2f} у.е. по {count} транзакциям. Попробуйте сократить траты в этой категории."
        )

    return recommendations

# === Рекомендация: часто нулевой баланс ===

def detect_low_balance(transactions):
    zero_balances = sum(1 for t in transactions if t["balance"] == 0)
    if zero_balances > 2:
        return "Ваш баланс часто опускается до нуля. Рекомендуем создать финансовую подушку безопасности."
    return None

# === Рекомендация: нестабильная зарплата ===

def detect_income_irregularity(transactions):
    salary_dates = [t["date_created"] for t in transactions if t["category"] == "Зарплата"]
    salary_months = {d[:7] for d in salary_dates}
    if len(salary_months) < 1:
        return "Мы не нашли регулярных доходов (зарплаты). Рекомендуем установить стабильный источник дохода."
    return None

# === Рекомендация: резкий рост расходов по категориям ===

def analyze_category_spikes(transactions, threshold=2.0):
    weekly_spend = defaultdict(lambda: defaultdict(float))  # category -> week -> amount

    for t in transactions:
        if t["delta"] < 0:
            week = week_key(t["date_created"])
            cat = t["category"]
            weekly_spend[cat][week] += -t["delta"]

    recommendations = []

    for cat, weeks in weekly_spend.items():
        sorted_weeks = sorted(weeks.items())
        for i in range(1, len(sorted_weeks)):
            prev_week, prev_val = sorted_weeks[i-1]
            curr_week, curr_val = sorted_weeks[i]
            if prev_val > 0 and curr_val / prev_val >= threshold:
                recommendations.append(
                    f"За неделю {curr_week} ваши расходы по категории '{cat}' выросли в {curr_val / prev_val:.1f} раза по сравнению с предыдущей неделей. Подумайте, можно ли это сократить."
                )

    return recommendations

# === Рекомендация: анализ долей категорий ===

def analyze_budget_shares(transactions, budget_thresholds=None):
    if budget_thresholds is None:
        budget_thresholds = {
            "Аренда": 0.5,
            "Еда": 0.4,
            "Одежда и обувь": 0.3
        }

    total_spent = 0
    category_spent = defaultdict(float)

    for t in transactions:
        if t["delta"] < 0:
            total_spent += -t["delta"]
            category_spent[t["category"]] += -t["delta"]

    recommendations = []

    for cat, share_limit in budget_thresholds.items():
        spent = category_spent.get(cat, 0)
        if total_spent > 0 and (spent / total_spent) >= share_limit:
            recommendations.append(
                f"Вы тратите {spent:.0f} у.е. ({(spent / total_spent * 100):.0f}%) на категорию '{cat}'. Это слишком много — подумайте о сокращении этих расходов."
            )

    return recommendations

# === Главная функция анализа ===

def analyze_transactions(transactions):
    recs = []

    recs += generate_recommendations(transactions)

    low_balance = detect_low_balance(transactions)
    if low_balance:
        recs.append(low_balance)

    income_check = detect_income_irregularity(transactions)
    if income_check:
        recs.append(income_check)

    recs += analyze_category_spikes(transactions)
    recs += analyze_budget_shares(transactions)

    return recs

# === Точка входа ===

def recomendate(data: list):
    recommendations = analyze_transactions(data)
    recommendations_json = [{"id": i + 1, "recommendation": r} for i, r in enumerate(recommendations)]
    return recommendations_json

if __name__ == "__main__":
    with open("response_1743856034424.json", "r", encoding="utf-8") as f:
        transactions = json.load(f)
    
    print(recomendate(transactions))
    recommendations = analyze_transactions(transactions)

    print("📊 Финансовые рекомендации:")
    for i, r in enumerate(recommendations, 1):
        print(f"{i}. {r}")

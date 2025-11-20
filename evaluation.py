import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

# --- 1. Функция очистки (та же, что и раньше) ---
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'0x[0-9a-f]+', '<ADDR>', text)
    text = re.sub(r'\d+', '<NUM>', text)
    text = re.sub(r'[^a-z\s\._\:\=\(\)\[\]]', ' ', text) # Добавили скобки [] для списков
    return text

# --- 2. Загрузка и Подготовка ---
print("Загрузка данных...")
try:
    df = pd.read_csv('error_dataset.csv')
except FileNotFoundError:
    print("Ошибка: Файл error_dataset.csv не найден. Запустите data_generator.py")
    exit()

# Чистим данные
df['clean_text'] = df['full_text'].apply(clean_text)

X = df['clean_text']
y = df['label']

# Разделяем: 80% обучение, 20% тест
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 3. Обучение (Пайплайн) ---
print("Обучение модели...")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
    ('clf', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1))
])

pipeline.fit(X_train, y_train)

# --- 4. Предсказание на тестовых данных ---
y_pred = pipeline.predict(X_test)

# --- 5. Визуализация (Confusion Matrix) ---
# Получаем список классов, чтобы подписи были верными
class_names = pipeline.classes_

# Строим матрицу
cm = confusion_matrix(y_test, y_pred, labels=class_names)

plt.figure(figsize=(10, 8))
# Рисуем тепловую карту (Heatmap)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)

plt.title('Матрицу ошибок: Классификация ошибок')
plt.ylabel('Истинный класс ')
plt.xlabel('Предсказанный класс ')

# Сохраняем график в файл (вставьте его в статью!)
plt.savefig('confusion_matrix.png', dpi=300)
print("\nГрафик сохранен как 'confusion_matrix.png'")

# --- 6. Текстовый отчет для статьи ---
print("\n=== Classification Report ===")
report = classification_report(y_test, y_pred, target_names=class_names)
print(report)

# Сохраняем отчет в текстовый файл
with open('report.txt', 'w') as f:
    f.write(report)
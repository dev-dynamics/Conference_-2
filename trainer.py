import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from collector import clean_text


def train_model():
    # 1. Загрузка данных
    try:
        df = pd.read_csv('error_dataset.csv')
    except FileNotFoundError:
        print("Сначала запустите collector.py для сбора данных!")
        return

    if len(df) < 5:
        print("Слишком мало данных. Добавьте больше примеров в collector.py")
        return

    df['clean_text'] = df['full_text'].apply(clean_text)
    
    X = df['clean_text']
    y = df['label']

    # 2. Создание пайплайна
    # TfidfVectorizer преобразует текст в матрицу признаков
    # GradientBoostingClassifier ищет паттерны
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))), 
        ('clf', GradientBoostingClassifier(n_estimators=50, learning_rate=0.1))
    ])

    # 3. Обучение (в реальной статье разделите на train/test)
    model_pipeline.fit(X, y)
    print("Модель успешно обучена!")

    # 4. Сохранение модели в файл
    with open('error_classifier.pkl', 'wb') as f:
        pickle.dump(model_pipeline, f)
        
if __name__ == "__main__":
    train_model()
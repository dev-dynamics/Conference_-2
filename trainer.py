import pandas as pd
import re
import pickle
# ИМПОРТЫ: Заменили LinearSVC на LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression # <--- НОВАЯ МОДЕЛЬ!
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from collector import clean_text 

def train_model():
    print("Загрузка и подготовка данных...")
    try:
        df = pd.read_csv('error_dataset.csv')
    except FileNotFoundError:
        print("Ошибка: Сначала запустите data_generator.py!")
        return
    
    df['clean_text'] = df['full_text'].apply(clean_text)
    
    X = df['clean_text']
    y = df['label']

    # 2. Создание Пайплайна
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3), 
            stop_words='english',
            min_df=2
        )),
        # Используем LogisticRegression, она быстрая, робастная и дает predict_proba!
        ('clf', LogisticRegression(random_state=42, solver='liblinear', multi_class='ovr')) 
    ])

    # 3. Обучение
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Обучение новой модели LogisticRegression...")
    model_pipeline.fit(X_train, y_train)
    print("Модель успешно обучена!")

    # 4. Сохранение
    with open('error_classifier.pkl', 'wb') as f:
        pickle.dump(model_pipeline, f)
        
if __name__ == "__main__":
    train_model()
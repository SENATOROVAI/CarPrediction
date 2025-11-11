# CarPrediction
predict car photos

1. show_1.ipynb - основная работа модели
обучена на 16 моделях машин

Ячейки
1. прогнать предсказания над набором картинок

2. визуализация предсказания модели

3. справочник меток

4. ячейка статистика по датасету

5. обучение модели

6. ячейка расчет метрик на val датасете

1.1 out/result - картинки с машинами с предсказаниями марок машин

2. runs/train10/results.csv - метрики качества

2.1 data/cars_002_learn_3/val/images - val датасет для проверки метрик качества

recall = 0.91 precision = 0.91

3. runs/detect/train28/results.png - графики обучения

4. runs/detect/train28/results.csv - метрики обучения по эпохам

5. runs/detect/train28/confusion_matrix.png - матрица ошибок

6. runs/detect/train28/weights/best.pt - веса модели
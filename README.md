# CarPrediction
<img width="450" height="1454" alt="изображение" src="https://github.com/user-attachments/assets/b456cb12-c881-40cc-87a6-b2bd435be817" />

Краткая информация:
54 - марки
10553 - фото
- источник https://github.com/SENATOROVAI/CarPrediction/blob/develop/show_1.ipynb

predict car photos

1. show_1.ipynb - основная работа модели
  обучена на 54 моделях машин
  
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

2. runs/detect/train28
  1. weights - веса обученной модели
  2. confusion_matrix.png - матрица ошибок модели
  3. results.png - графики обучения модели
  4. results.csv - таблица лоссов и метрик обучения модели на каждой эпохе

3. data/cars_002_learn_3 - датасет с изображениями автомобилей
4. data_in/ - необработанные изображения из парсинга
5. out/result - результаты работы модели с изображениями
6. convert_images.py - преобразование фото в единый jpg формат
7. util.py - функции для инференса модели, используемые в show_1.ipynb
8. Отчет.docx - отчет о проделанной работе



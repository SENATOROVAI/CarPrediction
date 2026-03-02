import os
import yaml
import torch
import numpy as np
from pathlib import Path
from typing import Union
from PIL.Image import Image
from dataclasses import dataclass, field

import ultralytics
from ultralytics import YOLO
from ultralytics.engine.results import Boxes



def predict_img(img: np.ndarray, model: YOLO) -> ultralytics.engine.results:
    """
    Предсказывает results по картинке.
    1. делает картинку с padding слева и справа
    2. предсказывает results, с учетом новых параметров imgsz, rect (НЕТРИВИАЛЬНО)
    3. меняет results - сдвигает влево на padding (НЕТРИВИАЛЬНО)
    4. убирает padding

    Parameters
    ----------
    img : np.ndarray
        картинка.
    model: YOLO
        модель, нейроматрица.

    Returns
    -------
    ultralytics.engine.results
        results
    """
    # 1. делает картинку с padding слева и справа
    padding=1000
    
    h, w = img.shape[:2]
    
    # Создаем изображение с паддингом
    # padded_image = np.full((h + 2*padding, w + 2*padding, 3), 114, dtype=np.uint8)
    # 114 - цвет padding
    padded_image = np.full((h, w + 2*padding, 3), 114, dtype=np.uint8) 
    # padded_image[padding:padding+h, padding:padding+w] = img
    padded_image[0:0+h, padding:padding+w] = img

    # 2. предсказывает results, с учетом новых параметров imgsz, rect (НЕТРИВИАЛЬНО)
    results = model.predict(padded_image,
        imgsz=2048,
        rect=False)

    # 3. меняет results - сдвигает влево на padding (НЕТРИВИАЛЬНО)
    for result in results:
        x_shift=padding
        y_shift=0
        for result in results:
            # 1. boxes
            if result.boxes is not None and len(result.boxes) > 0:
                # Получаем текущие координаты
                boxes_data = result.boxes.data.clone()

                # Сдвигаем координаты
                boxes_data[:, 0] -= x_shift  # x1
                boxes_data[:, 1] -= y_shift  # y1
                boxes_data[:, 2] -= x_shift  # x2
                boxes_data[:, 3] -= y_shift  # y2
            
                # # Создаем новые Boxes с обновленными координатами
                from ultralytics.engine.results import Boxes

                new_boxes = Boxes(boxes_data, result.orig_shape)
                # new_boxes = Boxes(
                #     new_xyxy,
                #     # original_xyxy,  # оригинальный формат
                #     result.boxes.conf,  # уверенности
                #     result.boxes.cls,   # классы
                #     result.boxes.data,  # все данные
                #     result.orig_shape   # размер оригинального изображения
                # )
                
                # # Заменяем boxes в результатах
                result.boxes = new_boxes

            # masks
            # _shift_masks(result.masks, x_shift, y_shift)
    
            # ! works 1
            # masks_data = result.masks.data.clone()
            # print(f'masks_data {masks_data}')  
            # masks_data[:, 0] -= x_shift  # x1
            # masks_data[:, 1] -= y_shift  # y1
            # print(f'masks_data 2 {masks_data}')  

            # for polygon in result.masks.xy:  
            #     print(f'polygon {polygon}')  
            # masks_2 = Masks(masks_data, result.orig_shape)
            # result.masks = masks_2
            # for polygon in result.masks.xy:  
            #     print(f'polygon {polygon}')  
            # ~

            # todo Magic numbers: 1000 -320
            # shift_yolo_masks(result, -325, -y_shift)

            # 2. polygon (segmentation)            
            if result.masks is not None and len(result.masks) > 0:
                for polygon in result.masks.xy:
                    # if isinstance(polygon, np.ndarray):
                    #     # polygon = torch.from_numpy(polygon).to(device)
                    #     polygon = torch.from_numpy(polygon)
                    # xy_tensors.append(polygon)
                    # print(f'polygon {polygon}')
                    for point in polygon:
                        # print(f'point {point}')
                        point[0] = point[0] + x_shift
                        point[1] = point[1] + y_shift
            # Debug
            # for polygon in result.masks.xy:
            #     # if isinstance(polygon, np.ndarray):
            #     #     # polygon = torch.from_numpy(polygon).to(device)
            #     #     polygon = torch.from_numpy(polygon)
            #     # xy_tensors.append(polygon)
            #     print(f'polygon {polygon}')
    
            # from ultralytics.engine.results import Masks

            # xy_tensors = []
            # for polygon in result.masks.xy:
            #     if isinstance(polygon, np.ndarray):
            #         # polygon = torch.from_numpy(polygon).to(device)
            #         polygon = torch.from_numpy(polygon)
            #     xy_tensors.append(polygon)
            
            # # Создаем masks объект
            # # masks_2 = Masks(xy_tensors, image_shape, device)
            # masks_2 = Masks(xy_tensors, result.orig_shape)
            # result.masks = masks_2

    # 4. убирает padding
    # поскольку отдаем results, картинку с padding не сдвигаем. Её сдвинет тот кому надо порисовать

    return results

# todo Define result type
# def show_results_img(result: ultralytics.engine.results) -> np.ndarray:
def show_results_img(result) -> np.ndarray:
    """
    Нарисовать картинку по result

    ! [WARNING] Это хак, который смещает bbox вправо на padding
    Надо переделать в общем виде
    """    
    padding=1000

    # 2. меняем bboxes
    x_shift = -padding
    y_shift = 0
    if result.boxes is not None and len(result.boxes) > 0:
        # Получаем текущие координаты
        boxes_data = result.boxes.data.clone()

        # Сдвигаем координаты
        boxes_data[:, 0] -= x_shift  # x1
        boxes_data[:, 1] -= y_shift  # y1
        boxes_data[:, 2] -= x_shift  # x2
        boxes_data[:, 3] -= y_shift  # y2
    
        # # Создаем новые Boxes с обновленными координатами

        new_boxes = Boxes(boxes_data, result.orig_shape)
        # new_boxes = Boxes(
        #     new_xyxy,
        #     # original_xyxy,  # оригинальный формат
        #     result.boxes.conf,  # уверенности
        #     result.boxes.cls,   # классы
        #     result.boxes.data,  # все данные
        #     result.orig_shape   # размер оригинального изображения
        # )
        
        # # Заменяем boxes в результатах
        result.boxes = new_boxes
    
    annotated_image = result.plot()
    
    # h, w = img.shape[:2]
    h, w = result.orig_img.shape[:2]
    
    # annotated_image_remove_padding = annotated_image[0:0+h, padding:padding+w]
    w = w - 2*padding
    annotated_image_remove_padding = annotated_image[0:0+h, padding:padding+w]
    
    return annotated_image_remove_padding
import os
from PIL import Image
from pathlib import Path

def convert_images_to_jpg(root_folder):
    """
    Конвертирует все изображения в папке и подпапках в формат JPG.
    
    Parameters:
    -----------
    root_folder : str
        Путь к корневой папке с изображениями
    """
    
    # Поддерживаемые форматы изображений
    supported_formats = {'.webp', '.png', '.jpeg', '.jpg', '.bmp', '.tiff', '.gif'}
    
    # Счётчики
    total_converted = 0
    total_skipped = 0
    total_errors = 0
    
    print("🔄 Начинаем конвертацию изображений...")
    print(f"📁 Корневая папка: {root_folder}\n")
    
    # Проходим по всем папкам и файлам
    for folder_path, _, files in os.walk(root_folder):
        folder_name = os.path.basename(folder_path)
        
        # Пропускаем корневую папку в выводе
        if folder_path == root_folder:
            continue
            
        # Фильтруем только изображения
        image_files = [f for f in files if Path(f).suffix.lower() in supported_formats]
        
        if not image_files:
            continue
            
        print(f"📂 Обработка папки: {folder_name} ({len(image_files)} файлов)")
        
        # Конвертируем каждое изображение
        for filename in image_files:
            file_path = os.path.join(folder_path, filename)
            
            # Если файл уже JPG, пропускаем
            if filename.lower().endswith('.jpg'):
                total_skipped += 1
                continue
            
            try:
                # Открываем изображение
                with Image.open(file_path) as img:
                    # Конвертируем в RGB (нужно для JPG)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Создаём белый фон для прозрачных изображений
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Создаём новое имя файла с расширением .jpg
                    name_without_ext = Path(filename).stem
                    new_filename = f"{name_without_ext}.jpg"
                    new_file_path = os.path.join(folder_path, new_filename)
                    
                    # Сохраняем как JPG
                    img.save(new_file_path, 'JPEG', quality=95, optimize=True)
                    
                    # Удаляем старый файл
                    os.remove(file_path)
                    
                    total_converted += 1
                    print(f"  ✅ {filename} → {new_filename}")
                    
            except Exception as e:
                total_errors += 1
                print(f"  ❌ Ошибка при конвертации {filename}: {e}")
    
    # Итоговая статистика
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТЫ КОНВЕРТАЦИИ:")
    print("="*60)
    print(f"✅ Конвертировано: {total_converted} файлов")
    print(f"⏭️  Пропущено (уже JPG): {total_skipped} файлов")
    print(f"❌ Ошибок: {total_errors} файлов")
    print(f"📝 Всего обработано: {total_converted + total_skipped + total_errors} файлов")
    print("="*60)

# Запуск конвертации
if __name__ == "__main__":
    # Путь к папке с изображениями
    root_folder = "data_in/google_dataset_cars"
    
    # Проверяем, существует ли папка
    if not os.path.exists(root_folder):
        print(f"❌ Папка {root_folder} не найдена!")
        print("💡 Убедитесь, что путь правильный.")
    else:
        convert_images_to_jpg(root_folder)
        print("\n✨ Конвертация завершена!")
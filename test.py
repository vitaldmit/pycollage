import os
import time
import asyncio
import aiofiles.os
import yadisk
from PIL import Image
from secret import YA_TOKEN

# Родительская директория где находятся списки с папками
root_folder: str = "Для тестового"
# Список с папками изображения в которых нехобходимо перевести в коллаж
folder_list: list[str] =  ['1388_12_Наклейки 3-D_3', '1369_12_Наклейки 3-D_3'] 
# Количество столбцов
columns: int = 4
# Отступ между изображениями в пикселях
padding: int = 100

# Функция создания коллажа
def create_collage(input_folder, output_file, cols=2, padding=10):
    # Получаем список всех изображений в указанной папке
    extensions: tuple[()] = ('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.webp', '.bmp', '.gif')
    image_files: list = [f for f in os.listdir(input_folder) if f.lower().endswith(extensions)]
    
    if not image_files:
        print(f"Нет файлов в указанной папке хотябы c одним расширением из {str(extensions)}")
        return
    
    # Открываем все изображения
    images = [Image.open(os.path.join(input_folder, f)) for f in image_files]
    
    # Определяем размеры коллажа
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    rows = (len(images) + cols - 1) // cols
    
    # Создаем новое изображение для коллажа с учетом отступов
    collage_width = (max_width * cols) + (padding * (cols + 1))
    collage_height = (max_height * rows) + (padding * (rows + 1))
    collage = Image.new('RGB', (collage_width, collage_height), color='white')
    
    # Размещаем изображения в коллаже с отступами
    for i, img in enumerate(images):
        x = (i % cols) * (max_width + padding) + padding
        y = (i // cols) * (max_height + padding) + padding
        collage.paste(img, (x, y))
    
    # Сохраняем коллаж в TIFF файл
    collage.save(output_file, format='TIFF')
    
    print(f"Создан коллаж в TIFF файле: {output_file}")

# Основная функция
async def main():
    async with yadisk.AsyncClient(token=YA_TOKEN, session="aiohttp") as client:
        # Проверяем, валиден ли токен
        if await client.check_token():
            print("Токен действителен")
        else:
            print("Токен недействителен")
            return

        # Функция просмотра содержимого
        async def list_files(folder_path):
            try:
                print(f"Содержимое папки {folder_path}:")
                async for item in await client.listdir(folder_path):
                    print(f" - {item.name} ({'(папка)' if item.type == 'dir' else '(файл)'})")
            except yadisk.exceptions.YaDiskError as e:
                print(f"Ошибка при получении списка файлов: {e}")

        # Функция скачивания файлов
        async def download_file(remote_path, local_path):
                # Создаем аналогичну директорию для скачивания файлов
                await aiofiles.os.makedirs(local_path, exist_ok=True)
                try:
                    async for file in await client.listdir(remote_path):
                        # print(f"{remote_path}{file.name}")
                        # print(f"{local_path}{file.name}")
                        await client.download(f"{remote_path}{file.name}", f"{local_path}{file.name}")
                        print(f"Файл '{remote_path}{file.name}' успешно скачан")
                except yadisk.exceptions.YaDiskError as e:
                    print(f"Ошибка при скачивании файла: {e}")

        # Получаем общую информацию о диске
        # print(await client.get_disk_info())

        # Cоздаем задачи
        tasks = [asyncio.create_task(download_file(f"{root_folder}/{folder}/", f"{folder}/")) for folder in folder_list]

        # Запускаем задачи
        for future in asyncio.as_completed(tasks):
            # получаем результаты по готовности 
            await future

        # Создаем коллажи
        for folder in folder_list:
            create_collage(folder, f"{folder}/{folder}.tif", columns, padding)


if __name__ == '__main__':
    start: float = time.time()

    asyncio.run(main())
    
    total: float = time.time() - start
    print(f'Общее время выполнения: {total:.3f} сек.')

# Скрипт собирает изображения из списка директорий в один `tiff` файл и сохраняет его в соответствующей директории под именем `{folder_name}.tif`.

Скрипт на скачивание файлов работает асинхронно.

**Для начала работы необходимо получить токен от яндекса**

Установка и настройка:
```bash
python -m venv test
cd test && . bin/activate && mkdir src && cd src
git clone https://github.com/vitaldmit/test_mycego.git .
pip install -r requirements.txt
cp secret_example.py secret.py # Insert your own token
```

Запуск скрипта
```bash
python test.py
```

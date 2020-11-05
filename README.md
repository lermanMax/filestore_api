## filestore_api  

Демонизация приложения реализованна через gunicorn. Для запуска можно использовать скрипт api_run.sh 

## Методы
### :black_medium_square: Upload
Метод сохраняет переданный файл

#### HTTP Request
```
POST http://127.0.0.1:8000/upload
```
``` python
requests.post("http://127.0.0.1:8000/upload", files = {"file": open('exemple.txt', 'rb')})
```


#### Response
Метод возвращает JSON следующей структуры
```
{
  "filehash": "hashhashhashhashhashhashhashhash"
}

```

### :black_medium_square: Download
Метод возвращает файл по переданному значению хэша

#### HTTP Request
```
POST http://127.0.0.1:8000/download
```
``` python
requests.get("http://127.0.0.1:8000/download", {'filehash': 'hashhashhashhashhashhashhashhash' })
```

```
{
  "filehash": "hashhashhashhashhashhashhashhash"
}
```

#### Response
content
```
b'<...binary code...>'

```
### :black_medium_square: Delete
Метод сохраняет переданный файл

#### HTTP Request
```
POST http://127.0.0.1:8000/delete
```
``` python
requests.delete("http://127.0.0.1:8000/delete", {'filehash': 'hashhashhashhashhashhashhashhash' })
```

```
{
  "filehash": "hashhashhashhashhashhashhashhash"
}
```
## Задача
Реализовать демон, который предоставит HTTP API
#### Upload:
- получив файл от клиента, демон возвращает в отдельном поле http
response хэш загруженного файла
- демон сохраняет файл на диск в следующую структуру каталогов:
     store/ab/abcdef12345...
где "abcdef12345..." - имя файла, совпадающее с его хэшем.
/ab/  - подкаталог, состоящий из первых двух символов хэша файла.
Алгоритм хэширования - на ваш выбор.

#### Download:
Запрос на скачивание: клиент передаёт параметр - хэш файла. Демон ищет
файл в локальном хранилище и отдаёт его, если находит.

#### Delete:
Запрос на удаление: клиент передаёт параметр - хэш файла. Демон ищет
файл в локальном хранилище и удаляет его, если находит.



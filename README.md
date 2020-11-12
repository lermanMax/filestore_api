# filestore_api  

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
  "filehash": "0123456789abcdef0123456789abcdef"
}

```

### :black_medium_square: Download
Метод возвращает файл по переданному значению хэша

#### HTTP Request
```
POST http://127.0.0.1:8000/download
```
``` python
requests.get("http://127.0.0.1:8000/download", {'filehash': '0123456789abcdef0123456789abcdef' })
```

```
{
  "filehash": "0123456789abcdef0123456789abcdef"
}
```

#### Response
content
```
b'<...binary code...>'

```
### :black_medium_square: Delete
Метод удаляет файл по переданному значению хэша

#### HTTP Request
```
POST http://127.0.0.1:8000/delete
```
``` python
requests.delete("http://127.0.0.1:8000/delete", {'filehash': '0123456789abcdef0123456789abcdef' })
```

```
{
  "filehash": "0123456789abcdef0123456789abcdef"
}
```

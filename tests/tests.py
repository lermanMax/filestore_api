"""
методы HTTP API:

Upload:
- получив файл от клиента, демон возвращает в отдельном поле http
response хэш загруженного файла
- демон сохраняет файл на диск в следующую структуру каталогов:
     store/ab/abcdef12345...
где "abcdef12345..." - имя файла, совпадающее с его хэшем.
/ab/  - подкаталог, состоящий из первых двух символов хэша файла.
Алгоритм хэширования - на ваш выбор.

Download:
Запрос на скачивание: клиент передаёт параметр - хэш файла. Демон ищет
файл в локальном хранилище и отдаёт его, если находит.

Delete:
Запрос на удаление: клиент передаёт параметр - хэш файла. Демон ищет
файл в локальном хранилище и удаляет его, если находит.
"""

import requests


url = "http://127.0.0.1:8000/"

class filestore_test:

    def __init__(self, url_base):
        self.url_base = url_base
        
    def upload(self, file_path):
        method = 'upload'   
        files = {'file': open(file_path, 'rb')} 
        response = requests.post(self.url_base + method, files=files)
        try:
            return response, response.json()['filehash']
        except:
            return response

    def download(self, filehash):
        method = 'download'
        params = {'filehash': filehash}
        response = requests.get(self.url_base + method, params=params)
        try:
            return response, response.json()
        except:
            return response
        
    def delete(self, filehash):
        method = 'delete'
        params = {'filehash': filehash}
        response = requests.delete(self.url_base + method, params=params)
        try:
            return response, response.json()
        except:
            return response    


test = filestore_test(url)


print('start upload tests')


print(test.upload('fileTest.txt'))



print('start download test')



print('start delete test')





'''
#headers = {
#    'cache-control': "no-cache",
#}
#cookies = {
#    'ASP.NET_SessionId': 'dbyn3xdli5iugqtn1oulkyik',
#    'BPOFLogin': '047FD1144C4400DD103E52BF4D13E31F42E6BFA1A94D78C7E53071B116418CBADC61597EE5F7369A21E22C1E33540691EC546FA950916342E530AE56BA80CEF0DB988ABC681C66A79F0A98EAF5009569EE0CC6FAD7E14E537652AE2E1BCD50C3DFDF9013DC7D6AA8E7F0358FA97526E9',
#}
#data = {
#    'some_input_name': 'some input value',
#    'another_input_name': 'another input value',
#}
#files = {
#    'some_file_name': open('file.jpg', 'rb')
#}
#
#r = requests.post(url, headers=headers, cookies=cookies, data=data, files=files)
'''
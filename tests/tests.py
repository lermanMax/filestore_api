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


url = "http://127.0.0.1:5000/"

class filestore_test:

    def __init__(self, url_base):
        self.url_base = url_base
        
    def upload(self, expected_code, file_path):
        method = 'upload'   
        files = {'file': open(file_path, 'rb')} 
        response = requests.post(self.url_base + method, files=files)
        
        result = '❌'
        if response.status_code == expected_code: result = '✅'
        
        try:
            return result, response.status_code, response.json()
        except:
            return result, response.content


    def download(self, expected_code, filehash):
        method = 'download'
        params = {'filehash': filehash}
        response = requests.get(self.url_base + method, params=params)
        
        result = '❌'
        if response.status_code == expected_code: result = '✅'
        
        try:
            return result, response.status_code
        except:
            return result, response.content
        
        
    def delete(self, expected_code, filehash):
        method = 'delete'
        params = {'filehash': filehash}
        response = requests.delete(self.url_base + method, params=params)
        
        result = '❌'
        if response.status_code == expected_code: result = '✅'
        
        try:
            return result, response.status_code
        except:
            return result, response.content    


test = filestore_test(url)



print('START upload tests')
print('test01 : ', test.upload(201, 'fileTest.txt'))
print('test02 : ', test.upload(409, 'fileTest.txt'))


print('____________________')
print('START download tests')
print('test01 : ', test.download(200, '33bd7853c56d9f4f2c78496822060c83'))
print('test02 : ', test.download(404, '00000000000000000000000000000000'))
print('test03 : ', test.download(400, '0000000000000000000000000'))
print('test04 : ', test.download(400, '../33bd7853c56d9f4f2c78496822060'))
print('test05 : ', test.download(404, '33BD7853c56d9f4f2c78496822060c83')) # ?? важен ли регистр
print('test06 : ', test.download(400, ''))
print('test07 : ', test.download(400, 12345678901234567890123456789012 ))


print('____________________')
print('START delete tests')
print('test01 : ', test.delete(204, '33bd7853c56d9f4f2c78496822060c83'))
print('test02 : ', test.delete(404, '00000000000000000000000000000000'))
print('test03 : ', test.delete(400, '0000000000000000000000000'))
print('test04 : ', test.delete(400, '../33bd7853c56d9f4f2c78496822060'))
print('test05 : ', test.delete(404, '33BD7853c56d9f4f2c78496822060c83'))
print('test06 : ', test.delete(400, ''))
print('test07 : ', test.delete(400,  12345678901234567890123456789012 ))




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
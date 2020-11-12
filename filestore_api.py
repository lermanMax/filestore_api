import os
import hashlib
import tempfile

from flask import Flask, send_from_directory
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.datastructures import FileStorage


app = Flask(__name__)
api = Api(app)

main_dir = './store/'


def hashing_file(path, block_size=4096): # Размер кластера по умолчанию для NTFS = 4KB
    hash_f = hashlib.md5() 
    with open(path,'rb') as f: 
        #читаем файл блоками по 4КВ, чтобы не держать файл целиком в памяти если он большой
        for block in iter(lambda: f.read(block_size), b''): 
            hash_f.update(block) 
    
    return hash_f.hexdigest()

def abort_if_bad_filehash(filehash): # проверка коректности данных
    hexdigits = '0123456789abcdefABCDEF'
    
    if (not filehash 
        or len(filehash) != 32 
        or not all(s in hexdigits for s in filehash)):
        
        abort(400, message="Bad request")  

def abort_if_file_doesnt_exist(path, filehash):
    if not os.path.exists(os.path.join(path, filehash)):
        abort(404, message="File {} doesn't exist".format(filehash))

def abort_if_file_exist(path, filehash):
    if os.path.exists(os.path.join(path, filehash)):
        abort(409, message="File already exist. It is available by this name: {}".format(filehash))
        
def delete_if_folder_is_empty(path):
    if not os.listdir(path):
        os.rmdir(path) #удаление пустого каталога

parser = reqparse.RequestParser()
parser.add_argument('file', type = FileStorage, location='files')
parser.add_argument('filehash')


class Upload(Resource):
    def post(self):
        args = parser.parse_args()
#        with tempfile.NamedTemporaryFile() as file:
        with tempfile.TemporaryDirectory(dir = main_dir) as dirname: # временная директория, удаляется со всем содержимым 
            temporary_save = os.path.join(dirname, 'temporary') # путь для временного сохранения файла
            args['file'].save(temporary_save)
            
            filehash = hashing_file(temporary_save)
            path = main_dir + filehash[0:2] #получаем новый путь. подпапка из перых двух символов хэша  
        
            abort_if_file_exist(path, filehash)
            
            os.renames(temporary_save, os.path.join(path, filehash)) #меняем имя и путь к файлу 
        return {'filehash': filehash}, 201

class Download(Resource):
    def get(self):
        args = parser.parse_args()
        filehash = args['filehash']
        path = main_dir + filehash[0:2]
        
        abort_if_bad_filehash(filehash)
        abort_if_file_doesnt_exist(path, filehash)
        
        return send_from_directory(path, filehash)
    
class Delete(Resource):
    def delete(self):
        args = parser.parse_args()
        filehash = args['filehash']
        path = main_dir + filehash[0:2] 
        
        abort_if_bad_filehash(filehash)
        abort_if_file_doesnt_exist(path, filehash)
        
        os.remove(os.path.join(path, filehash))         
        delete_if_folder_is_empty(path) #удалить директорию, если она пуста после удаления файла
        return '', 204 

    
api.add_resource(Upload, '/upload')
api.add_resource(Download, '/download')
api.add_resource(Delete, '/delete')


if __name__ == '__main__':
    app.run(debug=True)

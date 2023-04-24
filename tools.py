import requests
import tempfile

# db imports
from data import models
from data.db_session import create_session

# User session imports
from flask import session
from flask_login import AnonymousUserMixin, current_user

from config import YANDEX_API_KEY


def create_file(file_data, container=None):
    """ 
    Create and return File obj 
    
    file_data: file data from flask_wtf.fields.FileField
    container: Container obj
    return: File obj
    """
    with create_session() as session:
        data = {
            'user_id': current_user.id,
            'name': file_data.filename,
            'is_displayable': file_data.filename.split('.')[-1] in ('png', 'jpg', 'jpeg', 'bmp', 'gif'),
        }
        file = models.File(**data)
        session.add(file)
        session.commit()  # commit for setting id
        
        path = f'user_files/{file.id}_{file_data.filename}'
        file.path = path
        file_data.save(f'static/{path}')
        if container is not None:
            container.files.extend([file])
        session.commit()
        return file



def get_map(user: models.User):
    def get_pos(user_: models.User):
        url = 'http://geocode-maps.yandex.ru/1.x/'
        params = {
            'apikey': YANDEX_API_KEY,
            'geocode': user_.address,
            'format': 'json'
        }
        response_ = requests.get(url, params=params).json()
        return response_['response']["GeoObjectCollection"]['featureMember'][0]['GeoObject']['Point']['pos'].split()
    
    url = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'l': 'map',
        'pt': '{},{},pm2bll'.format(*get_pos(user))
    }
    if isinstance(current_user, AnonymousUserMixin) or user.id == current_user.id:
        params['spn'] = '0.1,0.1'
    else:
        if current_user.address:
            params['pt'] += '~{},{},pm2dol'.format(*get_pos(current_user))
        else:
            params['spn'] = '0.1,0.1'
    response = requests.get(url, params=params)
    print(response.url)
    return response.content
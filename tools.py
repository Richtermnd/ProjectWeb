from functools import wraps

# db imports
from data import models
from data.db_session import create_session

# User session imports
from flask import session
from flask_login import current_user


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

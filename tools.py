# db imports
from data import models
from data.db_session import create_session

# User session imports
from flask_login import current_user


def create_file(file_data, container=None):
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
        with open(f'static/{path}', mode='wb') as f:
            f.write(file_data.read())
        if container is not None:
            container.files.apppend(file)
        session.commit()
    return file
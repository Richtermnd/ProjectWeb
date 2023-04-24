from .user_resources import UserResources, UserListResources


def init(api):
    api.add_resource(UserResources, '/api/users/<int:user_id>')
    api.add_resource(UserListResources, '/api/users')

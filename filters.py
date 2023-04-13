app = None


def sort_chats(_chats):
    empty_chats = list(filter(lambda x: x.last_message is None, _chats))
    chats = list(filter(lambda x: x.last_message is not None, _chats))
    chats.sort(key=lambda x: x.last_message)
    return chats + empty_chats


def init(_app):
    global app
    app = _app

    app.jinja_env.filters['sort_chats'] = sort_chats
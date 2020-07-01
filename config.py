import os


class Config(object):
    SECRET_KY = os.environ.get('SECRET_KEY') or "b'vY\x12\xe9$\xa2\xa8M\\d\xa9+\xf3\x1c\xec8'"

    MONGODB_SETTINGS = {'db': 'hospital'}

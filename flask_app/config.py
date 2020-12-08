class Config:
    algod_api_address = 'https://testnet-algorand.api.purestake.io/ps2'
    algod_token = 'lGcdUfEiuN8JIetcoO3q87xfn9PZuP8p6057Qcgf'
    algod_public_key = 'KP7O7HDI6HJMWMLDE2PG5XIYHVVDNLDTBEZ4ON37GMT5SMFPUYO7HOHX7Q'
    algod_private_key = 'QLmIu/0/0R/2+Ik0PF+zA86WwTbep5kwIAIF/imqV6tT/u+caPHSyzFjJp5u3Rg9ajascwkzxzd/MyfZMK+mHQ=='
    algod_mnemonic = "chimney carry tape zone pen margin sibling measure make language super then collect race vast " \
                     "pond basket liar library theory fault tunnel follow absent evidence "
    allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    flask_port = 5000
    flask_static_url_path = '/flask_app'
    ipfs_api_address = 'http://192.168.137.62:5001'


class BaseConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'do-i-really-need-this'
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY
    UPLOAD_FOLDER = './download'


class ProductionConfig(BaseConfig):
    DEVELOPMENT = False
    DEBUG = False

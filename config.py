import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Class to store config/env values to separate them from the main package. """

    # use it later when auth is implemented
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my-little-secret-key"
    # flask migrate doesn't seem to work using f-strings, learned the hard way (port issues)
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, 'g_helper.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DICT_ITEMS_PER_PAGE = 25
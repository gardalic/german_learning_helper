import os


class Config(object):
    """ Class to store config/env values to separate them from the main package. """

    # use it later when auth is implemented
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my-little-secret-key"

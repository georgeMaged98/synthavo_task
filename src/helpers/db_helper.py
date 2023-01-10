from flask_sqlalchemy import SQLAlchemy

class _DBHelper:
    instance = None

def DBHelper():
    if _DBHelper.instance is None:
        _DBHelper.instance = SQLAlchemy()
    return _DBHelper.instance


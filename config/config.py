from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).parent.parent
config = dotenv_values('.env')


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / 'database' / 'app.db.sqlite')
    SECRET_KEY = config['SECRET_KEY']

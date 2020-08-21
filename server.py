from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import template
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
DB_PATH = "sqlite:///albums.sqlite3"
class AlbumDB(Base):
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

@route('/')
def openIndex():
    try:
        return template('index.html')
    except HTTPError as e:
        errorStr = 'index.html не найден!</br>{}'.format(e)
        return errorStr


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
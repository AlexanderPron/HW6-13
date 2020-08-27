from bottle import route, request
from bottle import run
from bottle import HTTPError
from bottle import get, post, static_file
import  json
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
        return static_file('index.html', root = './static/')
    except Exception as e:
        errorStr = 'index.html не найден!</br>{}'.format(e)
        return errorStr

@route('/', method = 'POST')
def getArtist():
    data = ["s1","s2","s3"] # Создать список из нашей БД
    return json.dumps(data)

@route('/static/<filename:path>')
def st(filename):
    return static_file(filename, root="./static/")

@route('/albums/', method = 'POST')
def displayAlbums():
    s = connectDB(DB_PATH)
    addAlbum(s)
    return "Данные нового альбома добавлены в БД\n"

def connectDB(path):
    engine = sa.create_engine(path)
    Sessions = sessionmaker(engine)
    session = Sessions()
    return session

def addAlbum(session):
    year = request.forms.get('albumYear')
    artist = request.forms.get('artistName')
    genre = request.forms.get('albumGenre')
    album = request.forms.get('albumName')
    newAlbum = AlbumDB(year = int(year), artist = artist, genre = genre, album = album)
    session.add(newAlbum)
    session.commit()




if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
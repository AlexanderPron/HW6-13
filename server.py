from bottle import route, request, response, run, HTTPError, get, post, static_file
import  json
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
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
    s = connectDB(DB_PATH)
    data = getArtists(s)
    return json.dumps(data)

@route('/static/<filename:path>')
def st(filename):
    return static_file(filename, root="./static/")

@route('/albums/', method = 'POST')
def addAlbumPage():
    s = connectDB(DB_PATH)
    addAlbum(s)
    try:
        return static_file('addAlbum.html', root = './static/')
    except Exception as e:
        errorStr = 'addAlbum.html не найден!</br>{}'.format(e)
        return errorStr

@route('/albums/<artist>', method = 'GET')
def displayAlbums(artist):
    s = connectDB(DB_PATH)
    data = getAlbums(s, artist)
    return json.dumps(data)
    # try:
    #     return static_file('addAlbum.html', root = './static/')
    # except Exception as e:
    #     errorStr = 'addAlbum.html не найден!</br>{}'.format(e)
    #     return errorStr

def connectDB(path):
    engine = sa.create_engine(path)
    Sessions = sessionmaker(engine)
    session = Sessions()
    return session

def addAlbum(session):
    # response.content_type = 'text/html; charset=UTF8'
    year = request.forms.getunicode('albumYear')
    artist = request.forms.getunicode('artistName')
    genre = request.forms.getunicode('albumGenre')
    album = request.forms.getunicode('albumName')
    newAlbum = AlbumDB(year = int(year), artist = artist, genre = genre, album = album)
    session.add(newAlbum)
    session.commit()
def getArtists(session):
    artists = []
    for art in session.query(func.distinct(AlbumDB.artist)):
        artists.append(art[0])
    return artists
def getAlbums(session, artist):  # Функция, которая на вход получает сессию и имя артиста/группы а на выходе отдает словарь {'count' : число альбомов исполнителя, 'исполнитель' : [список альбомов исполнителя]}
    rezJSON = {}
    artistAlbums = []
    albums = session.query(AlbumDB).filter(AlbumDB.artist == artist).all()
    count = session.query(AlbumDB).filter(AlbumDB.artist == artist).count()
    for album in albums:
        artistAlbums.append(album.album)
    rezJSON = {'count' : count, '{}'.format(artist) : artistAlbums}
    return rezJSON





if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
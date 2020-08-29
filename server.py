from bottle import route, request, response, run, HTTPError, get, post, static_file
import  json
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import datetime
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
    if addAlbum(s) == 1:
        try:
            return static_file('addAlbum.html', root = './static/')
        except Exception as e:
            errorStr = 'addAlbum.html не найден!</br>{}'.format(e)
            return errorStr
    if addAlbum(s) == 2:
        return 'Введён неверный год выпуска альбома. Год должен быть числом больше 1700 и меньше, либо равен текущему году '
    if addAlbum(s) == 3:
        return HTTPError(409, 'Альбом данного исполнителя уже в базе')

@route('/albums/<artist>', method = 'GET')
def displayAlbums(artist):
    s = connectDB(DB_PATH)
    data = getAlbums(s, artist)
    albums = data[artist]
    formatStr = ''
    for album in albums:
        formatStr += album + '</br>' 
    countAlbumStr = make_russian(data['count'])
    html = '''  <h2>Результат выборки из БД:</h2></br><hr>
                <p>У исполнителя '''+ artist + ''' в нашей бд ''' + countAlbumStr +''' :</br>'''+ formatStr + '''</p></br><a href="/">Назад</a>'''
    return html

def connectDB(path):
    engine = sa.create_engine(path)
    Sessions = sessionmaker(engine)
    session = Sessions()
    return session

def addAlbum(session):
    year = request.forms.getunicode('albumYear')
    artist = request.forms.getunicode('artistName')
    genre = request.forms.getunicode('albumGenre')
    album = request.forms.getunicode('albumName')
    flag = 1
    if validateYear(year) and (not isAlbumInDB(session, album, artist)):
        newAlbum = AlbumDB(year = int(year), artist = artist, genre = genre, album = album)
        session.add(newAlbum)
        session.commit()
        flag = 1  # Год верный и альбома данного исполнителя нет в бд
        return flag
    else:
        if not validateYear(year):
            flag = 2 # Год не верный
            return flag
        else: 
            if isAlbumInDB(session, album, artist):
                flag = 3 # Альбом данного исполнителя есть в бд
                return flag


def getArtists(session):
    artists = []
    for art in session.query(sa.func.distinct(sa.func.lower(AlbumDB.artist))):
        artists.append(art[0].title())
    return artists
def getAlbums(session, artist):  # Функция, которая на вход получает сессию и имя артиста/группы а на выходе отдает словарь {'count' : число альбомов исполнителя, 'исполнитель' : [список альбомов исполнителя]}
    rezJSON = {}
    artistAlbums = []
    albums = session.query(AlbumDB).filter(sa.func.lower(AlbumDB.artist) == sa.func.lower(artist)).all()
    count = session.query(AlbumDB).filter(sa.func.lower(AlbumDB.artist) == sa.func.lower(artist)).count()
    for album in albums:
        artistAlbums.append(album.album.title())
    rezJSON = {'count' : count, '{}'.format(artist) : artistAlbums}
    return rezJSON

def make_russian(albumNumber):  
    rus_str = ''   
    if albumNumber % 20 in [0,5,6,7,8,9,10,11,12,13,15,16,17,18,19]:
        rus_str = '{} альбомов'.format(albumNumber)
    if albumNumber % 20 in [2,3,4,14]:
        rus_str = '{} альбома'.format(albumNumber)
    if albumNumber % 20 in [1]:
        rus_str = '{} альбом'.format(albumNumber)
    if albumNumber == 14:
        rus_str = '{} альбомов'.format(albumNumber)
    return rus_str

def validateYear(year):
    try:
        if (int(year) >= 1700) and (int(year) <= datetime.datetime.now().year):
            return True
    except Exception:
        return False
    else:
        return False

def isAlbumInDB(session, album, artist):
    # SELECT * FROM album WHERE LOWER(album) = LOWER('BeggaRs bAnquet');
    findAlbums = session.query(AlbumDB).filter(sa.func.lower(AlbumDB.album) == sa.func.lower(album), sa.func.lower(AlbumDB.artist) == sa.func.lower(artist)).first()
    if findAlbums:
        return True
    else:
        return False






if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
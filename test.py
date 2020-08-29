from bottle import route, request
from bottle import run
from bottle import HTTPError
from bottle import get, post, static_file
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

def connectDB(path):
    engine = sa.create_engine(path, encoding='utf-8')
    Sessions = sessionmaker(engine)
    session = Sessions()
    return session

def getArtists(session):
    artists = []
    for art in session.query(func.distinct(AlbumDB.artist)):
        artists.append(art[0])
    return artists

def getAlbums(session, artist):
    # select * from album where artist = "Кино";
    # select count(album) from album where artist = "Кино";
    # self.closeByHeightAthelete = self.session.query(AtheleteDB).filter(AtheleteDB.height > 0).order_by(sa.func.abs(AtheleteDB.height*100 - self.userHeight)).first()
    albums = session.query(AlbumDB).filter(AlbumDB.artist == artist).all()
    count = session.query(AlbumDB).filter(AlbumDB.artist == artist).count()
    for album in albums:
        print(album.album)
    print(count)

def validateYear(year):
    print(datetime.datetime.now().year)
    try:
        if (int(year) >= 1700) and (int(year) <= datetime.datetime.now().year):
            return True
    except Exception:
        return False
    else:
        return False

def isAlbumInDB(session, album):
    # SELECT * FROM album WHERE LOWER(album) = LOWER('BeggaRs bAnquet');
    findAlbums = session.query(AlbumDB).filter(sa.func.lower(AlbumDB.album) == sa.func.lower(album)).first()
    if findAlbums:
        return True
    else:
        return False





def main():
    s = connectDB(DB_PATH)
    # rez = getArtists(s)
    # print(rez)
    # getAlbums(s, "Кино")
    # year = '1701er'
    # print(validateYear(year))
    print(isAlbumInDB(s, 'Beggars bAnquet'))

if __name__ == "__main__":
    main()
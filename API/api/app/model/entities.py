from sqlalchemy import Column, String, VARCHAR, LargeBinary, INTEGER, ForeignKey, ForeignKeyConstraint
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    username = Column(VARCHAR(length=20), name="username", primary_key=True, index=True)
    hashed_password = Column(LargeBinary, name='password')
    profile_image_url = Column(String, name='profile_image', default="/hearit_api/app/images/perfil.png")


class Playlist(Base):
    __tablename__ = "playlist"

    name = Column(VARCHAR(length=20))
    owner_username = Column(VARCHAR(length=20))
    id = Column(VARCHAR(length=20), primary_key=True, index=True)
    song_count = Column(INTEGER)


class Song(Base):
    __tablename__ = "song"

    name = Column(VARCHAR(length=20))
    singer = Column(VARCHAR(length=20))
    id = Column(VARCHAR(length=20), primary_key=True, index=True)
    url = Column(VARCHAR(length=255))
    concert_location = Column(VARCHAR(length=255))
    concert_date = Column(VARCHAR(length=20))


class PlaylistSongs(Base):
    __tablename__ = "playlist_songs"

    playlist_id = Column(VARCHAR(length=20), ForeignKey("playlist.id"), primary_key=True)
    song_id = Column(VARCHAR(length=20), ForeignKey("song.id"), primary_key=True)

    playlist = relationship('Playlist')
    song = relationship('Song')

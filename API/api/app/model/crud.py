from sqlalchemy.engine import row
from sqlalchemy.orm import Session
from sqlalchemy import asc, func
from . import entities
from .. import api_models



# ---------------------------  USER ------------------------------

def get_user(db: Session, username: str) -> entities.User | None:
    return db.query(entities.User).filter(entities.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[row]:
    return db.query(entities.User).offset(skip).limit(limit).all()


def get_user_password(db: Session, username: str) -> bytes | None:
    result = db.query(entities.User.hashed_password).filter(entities.User.username == username).first()
    return result.hashed_password if result else None



def create_user(db: Session, user: api_models.UserAuth) -> entities.User | None:
    if get_user(db, username=user.username):
        return None
    else:
        db_user = entities.User(username=user.username, hashed_password=user.hashed_password())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user



# ---------------------- PLAYLIST -----------------------------------

def get_user_playlists(db: Session, username: str) -> entities.Playlist | None:
    return db.query(entities.Playlist).filter(entities.Playlist.owner_username == username).all()

def create_playlist(db: Session, playlist: api_models.PlaylistCreate):
    db_playlist= entities.Playlist(name=playlist.name, owner_username=playlist.owner_username, id=playlist.id, song_count=playlist.song_count)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

def get_playlist(db: Session, playlist_id: str) -> entities.Playlist | None:
    return db.query(entities.Playlist).filter(entities.Playlist.id == playlist_id).first()

def edit_playlist(db: Session, playlist: entities.Playlist, playlist_name: str):
    playlist.name=playlist_name
    db.commit()
    db.refresh(playlist)
    return playlist


def delete_playlist(db: Session, playlist: entities.Playlist):
    db.delete(playlist)
    db.commit()
    return playlist

def clean_playlists(db: Session, username: str):
    db.query(entities.Playlist).filter(entities.Playlist.owner_username == username).delete()
    db.commit()

# ---------------------- SONGS -----------------------------------


def get_songs(db: Session) -> list[row]:
    return db.query(entities.Song).order_by(asc(entities.Song.name)).all()

def get_song(db: Session, song_id: str) -> entities.Song | None:
    return db.query(entities.Song).filter(entities.Song.id == song_id).first()


# ---------------------- PLAYLIST SONGS -----------------------------------

def get_playlistsSongs(db: Session, username: str) -> list[row]:
    return (db.query(entities.PlaylistSongs).join(entities.Playlist, entities.Playlist.id == entities.PlaylistSongs.playlist_id).filter(entities.Playlist.owner_username == username).all())

def get_playlistSongs(db: Session, playlist_id: str) -> list[row]:
    return db.query(entities.Song).join(entities.PlaylistSongs).filter(entities.PlaylistSongs.playlist_id == playlist_id).order_by(asc(entities.Song.name)).all()


def add_playlistSong(db: Session, playlist_id: str, song_id: str):
    db_playlist_song= entities.PlaylistSongs(playlist_id=playlist_id, song_id=song_id)
    db.add(db_playlist_song)
    db.commit()
    db.refresh(db_playlist_song)
    return db_playlist_song

def get_playlistSong(db: Session, playlist_id: str, song_id: str) -> entities.PlaylistSongs | None:
    return db.query(entities.PlaylistSongs).filter((entities.PlaylistSongs.playlist_id == playlist_id) &(entities.PlaylistSongs.song_id == song_id)).first()


def delete_playlistSong(db: Session, playlistSong: entities.PlaylistSongs):
    db.delete(playlistSong)
    db.commit()
    return playlistSong


def clean_playlistSongs(db: Session, username: str):
    db.query(entities.PlaylistSongs).filter(entities.PlaylistSongs.playlist.has(owner_username=username)).delete(synchronize_session=False)
    db.commit()


# ---------------------- IMÁGENES -----------------------------------

def get_user_profile_image_url(db: Session, username: str) -> str | None:
    result = db.query(entities.User.profile_image_url).filter(entities.User.username == username).first()
    return result.profile_image_url if result else result


def set_user_profile_image_url(db: Session, user: str | entities.User, url: str) -> bool:
    if isinstance(user, str):
        user = get_user(db, user)

    if user:
        user.profile_image_url = url
        db.commit()
        db.refresh(user)

    return bool(user)
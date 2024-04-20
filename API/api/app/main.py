from . import api_models
from fastapi import FastAPI, status, HTTPException, Depends, UploadFile
from fastapi.responses import RedirectResponse, FileResponse
from .model.database import get_db
from sqlalchemy.orm import Session
from .model import crud
from fastapi.security import OAuth2PasswordRequestFormStrict
import bcrypt
import firebase_admin
from firebase_admin import credentials, messaging
from unidecode import unidecode
from os import environ
from .api_models import Message, FirebaseClientToken
from mimetypes import guess_extension
from pathlib import Path


app = FastAPI()

cred = credentials.Certificate(environ['FIREBASE_CREDENTIALS'])
firebase_admin.initialize_app(cred)



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')



# ---------------------------  USER ------------------------------

@app.post("/identificate", response_model=api_models.User, status_code=status.HTTP_200_OK, tags=['Authentication'])
async def identificar(user: api_models.UserAuth, db: Session = Depends(get_db)):
    hashed_password = crud.get_user_password(db, username=user.username)

    if hashed_password is None or not bcrypt.checkpw(user.password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=404, detail="User or password is not correct.")

    return crud.get_user(db,user.username)



@app.post("/users", tags=["Users"],response_model=api_models.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: api_models.UserAuth, db: Session = Depends(get_db)):
    if not (db_user := crud.create_user(db=db, user=user)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return db_user



# ---------------------- PLAYLIST -----------------------------------

@app.get("/userPlaylists", response_model=list[api_models.Playlist], status_code=status.HTTP_200_OK, tags=["Playlists"])
async def get_user_playlists( user: str, db: Session = Depends(get_db)):
    if not (crud.get_user(db, user)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")
    return crud.get_user_playlists(db, user)


@app.post("/createPlaylist", tags=["Playlists"],
          response_model=api_models.Playlist, status_code=status.HTTP_201_CREATED)
async def create_playlist(playlist: api_models.PlaylistCreate, db: Session = Depends(get_db)):
    if (playlist_id := crud.get_playlist(db=db, playlist_id=playlist.id)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Playlist with that id already exists.")
    return crud.create_playlist(db, playlist)

@app.post("/editPlaylist", tags=["Playlists"],
          response_model=api_models.Playlist, status_code=status.HTTP_200_OK)
async def edit_playlist(playlist_id: str, playlist_name: str, db: Session = Depends(get_db)):
    if not (playlist := crud.get_playlist(db, playlist_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist doesn't exists.")

    return crud.edit_playlist(db, playlist, playlist_name)


@app.post("/deletePlaylist", tags=["Playlists"],
          response_model=api_models.Playlist, status_code=status.HTTP_200_OK)
async def delete_playlist(playlist_id: str, db: Session = Depends(get_db)):
    if not (playlist := crud.get_playlist(db, playlist_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist doesn't exists.")

    return crud.delete_playlist(db, playlist)


# ---------------------- SONGS -----------------------------------

@app.get("/songs", response_model=list[api_models.Song], status_code=status.HTTP_200_OK, tags=["Songs"])
async def get_songs( db: Session = Depends(get_db)):
    return crud.get_songs(db)
    

# ---------------------- PLAYLIST SONGS -----------------------------------

@app.get("/playlistsSongs", response_model=list[api_models.PlaylistSongs], status_code=status.HTTP_200_OK, tags=["PlaylistSongs"])
async def get_playlistsSongs(user: str, db: Session = Depends(get_db)):
    return crud.get_playlistsSongs(db, user)


@app.get("/playlistSongs", response_model=list[api_models.Song], status_code=status.HTTP_200_OK, tags=["PlaylistSongs"])
async def get_playlistSongs(playlist_id: str, db: Session = Depends(get_db)):
    if not (playlist := crud.get_playlist(db, playlist_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist doesn't exists.")

    return crud.get_playlistSongs(db, playlist_id)


@app.post("/addPlaylistSong", response_model=api_models.PlaylistSongs, status_code=status.HTTP_200_OK, tags=["PlaylistSongs"])
async def add_playlistSong(playlist_id: str, song_id: str, db: Session = Depends(get_db)):
    if not (playlist := crud.get_playlist(db, playlist_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist doesn't exists.")

    if not (song := crud.get_song(db, song_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song doesn't exists.")

    if (playlistSong := crud.get_playlistSong(db, playlist_id, song_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song is alredy in that playlist.")

    return crud.add_playlistSong(db, playlist_id, song_id)


@app.post("/deletePlaylistSong", tags=["PlaylistSongs"],response_model=api_models.PlaylistSongs, status_code=status.HTTP_200_OK)
async def delete_playlistSong(playlist_id: str, song_id: str, db: Session = Depends(get_db)):
    if not (playlist := crud.get_playlist(db, playlist_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist doesn't exists.")

    if not (song := crud.get_song(db, song_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song doesn't exists.")

    if not (playlistSong := crud.get_playlistSong(db, playlist_id, song_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song isn't in that playlist.")

    return crud.delete_playlistSong(db, playlistSong)




# --------------------------- NOTIFICACIONES ------------------------------

@app.post('/notifications/subscribe', status_code=status.HTTP_202_ACCEPTED, tags=["Notifications"])
def suscribe_user_to_alert(token: FirebaseClientToken):
    messaging.subscribe_to_topic([token.fcm_client_token], 'All')


async def send_notification(message: Message, topic: str = 'All'):
    messaging.send(
        messaging.Message(
            data={k: f'{v}' for k, v in dict(message).items()},
            topic=unidecode(topic.replace(' ', '_'))
        )
    )

    messaging.send(
        messaging.Message(
            notification=messaging.Notification(
                **dict(message)
            ),
            topic=unidecode(topic.replace(' ', '_'))
        )
    )


@app.post("/notifications", tags=["Notifications"])
async def send_broadcast_notification(message: Message):
    await send_notification(message)



# ---------------------- IMÁGENES -----------------------------------
@app.get("/profile/image", tags=["Users"],status_code=status.HTTP_200_OK, response_class=FileResponse)
async def get_user_profile_image(user: str, db: Session = Depends(get_db)):
    if not (user_profile_image_url := crud.get_user_profile_image_url(db, username=user)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")

    if Path(user_profile_image_url).exists():
        return FileResponse(user_profile_image_url, filename=Path(user_profile_image_url).name)
    else:
        return FileResponse("/hearit_api/app/images/placeholder.png", filename="placeholder.png")

VALID_IMAGE_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp']

@app.put("/profile/image", tags=["Users"],status_code=status.HTTP_200_OK)
async def set_user_profile_image(file: UploadFile, user: str, db: Session = Depends(get_db)):
    if not (user := crud.get_user(db, user)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")

    if file.content_type not in VALID_IMAGE_MIME_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File is not a valid image file. Valid types: {', '.join(VALID_IMAGE_MIME_TYPES)}")

    file_extension = guess_extension(file.content_type)
    path = f'/hearit_api/app/images/{user.username}{file_extension}'

    if crud.set_user_profile_image_url(db, user, path):
        contents = await file.read()
        with open(path, 'wb') as f:
            f.write(contents)





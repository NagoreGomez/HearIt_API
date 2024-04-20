import bcrypt
from pydantic import BaseModel


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserAuth(User):
    password: str

    def hashed_password(self) -> bytes:
        bytePwd = self.password.encode('utf-8')

        # Hash password with salt
        return bcrypt.hashpw(bytePwd, bcrypt.gensalt())



class Playlist(BaseModel):
    name: str
    owner_username: str
    id: str
    song_count: int


    class Config:
        orm_mode = True

class PlaylistCreate(Playlist):
    pass


class Song(BaseModel):
    name: str
    singer: str
    id: str
    url: str
    concert_location: str
    concert_date: str
    

    class Config:
        orm_mode = True



class PlaylistSongs(BaseModel):
    playlist_id: str
    song_id: str
    

    class Config:
        orm_mode = True


class Message(BaseModel):
    title: str
    body: str | None

class FirebaseClientToken(BaseModel):
    fcm_client_token: str
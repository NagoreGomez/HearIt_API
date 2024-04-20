CREATE TABLE users
(
    username        VARCHAR(20),
    password        bytea,
    profile_image   TEXT DEFAULT '/hearit_api/app/images/perfil.png',
    PRIMARY KEY (username)
);


CREATE TABLE playlist
(
    name                VARCHAR(20),
    owner_username      VARCHAR(20),
    id                  VARCHAR(20),
    song_count          smallint,
    PRIMARY KEY (id)
);



CREATE TABLE song
(
    name                VARCHAR(20),
    singer              VARCHAR(20),
    id                  VARCHAR(20),
    url                 VARCHAR(255),
    concert_location    VARCHAR(255),
    concert_date        VARCHAR(20),
    PRIMARY KEY (id)
);


CREATE TABLE playlist_songs
(
    playlist_id                VARCHAR(20),
    song_id                    VARCHAR(20),
    PRIMARY KEY (playlist_id,song_id)
);

CREATE OR REPLACE FUNCTION update_song_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE playlist
    SET song_count = (
        SELECT COUNT(*)
        FROM playlist_songs
        WHERE playlist_songs.playlist_id = NEW.playlist_id
    )
    WHERE id = NEW.playlist_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_playlist_song_count
AFTER INSERT OR DELETE ON playlist_songs
FOR EACH ROW
EXECUTE FUNCTION update_song_count();


INSERT INTO users (username, password) VALUES ('root', '$2b$12$qmRWcn46PJcwLGzsQsSFr.AkLIudco6NPdiY1wHWa.sVvjZVgAtyi');


INSERT INTO playlist (name, owner_username, id, song_count) VALUES ('Trabajo', 'root', '1', 0);
INSERT INTO playlist (name, owner_username, id, song_count) VALUES ('Coche', 'root', '2', 0);



INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Telepatía', 'Kali Uchis', '1', 'https://www.youtube.com/watch?v=Dwzk-XZxZ4k', 'Av. de Concha Espina, 1, 28036 Madrid, España', '03/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Diamonds', 'Rihanna', '2', 'https://www.youtube.com/watch?v=lWA2pjMjpBs', 'Passeig Olímpic, 5-7, 08038 Barcelona, España', '04/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Shape of My Heart', 'Sting', '3', 'https://www.youtube.com/watch?v=NlwIDxCjL-8', 'Av. de Felipe II, s/n, Salamanca, 28009 Madrid', '29/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Hotel California', 'Eagles', '4', 'https://www.youtube.com/watch?v=09839DpTctU', 'Av. de Concha Espina, 1, 28036 Madrid, España', '10/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Dancing Queen', 'ABBA', '5', 'https://www.youtube.com/watch?v=xFrGuyw1V8s', 'C. del Príncipe de Vergara, 146, 28002 Madrid, España', '11/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Highway to Hell', 'AC/DC', '6', 'https://www.youtube.com/watch?v=l482T0yNkeo', 'C. d Aristides Maillol, 12, 08028 Barcelona, España', '17/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Rolling in the Deep','Adele','7','https://www.youtube.com/watch?v=rYEDA3JcQqw','Av. de Felipe II, s/n, Salamanca, 28009 Madrid','18/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Wonderful Tonight','Eric Clapton','8','https://www.youtube.com/watch?v=UprwkbzUX6g','11 Avenue Raymond Badiou, 31300 Toulouse, Francia','24/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Like a Rolling Stone','Bob Dylan','9','https://www.youtube.com/watch?v=IwOfCgkyEj0','Passeig Olímpic, 5-7, 08038 Barcelona, España','25/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Unwritten','Natasha Bedingfield','10','https://www.youtube.com/watch?v=b7k0a5hYnSI','C. del Príncipe de Vergara, 146, 28002 Madrid, España','01/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Thinking Out Loud','Ed Sheeran','11','https://www.youtube.com/watch?v=lp-EO5I60KA','Piazzale dello Sport, 00144 Roma RM, Italia','15/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Halo','Beyonce','12','https://www.youtube.com/watch?v=bnVUHWCynig','ZAC du Cornillon Nord, 93216 Saint-Denis, Francia','24/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Shake It Off','Taylor Swift','13','https://www.youtube.com/watch?v=nfWlot6h_JM','8 Boulevard de Bercy, 75012 París, Francia','31/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Perfect','Ed Sheeran','14','https://www.youtube.com/watch?v=2Vv-BfVoq4g','211 Avenue Jean Jaurès, 75019 París, Francia','07/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Uptown Funk','Bruno Mars','15','https://www.youtube.com/watch?v=OPf0YbXqDm0','163 Boulevard du Mercantour, 06200 Niza, Francia','28/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Hey Jude','The Beatles','16','https://www.youtube.com/watch?v=A_MjCqQoLLA','Piazzale Angelo Moratti, 20151 Milán MI, Italia','22/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Thriller','Michael Jackson','17','https://www.youtube.com/watch?v=4V90AmXnguw','Piazzale dello Sport, 00144 Roma RM, Italia','03/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Stairway to Heaven','Led Zeppelin','18','https://www.youtube.com/watch?v=QkF3oxziUI4','Via Giuseppe di Vittorio, 6, 20090 Asesoría MI, Italia','25/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Billie Jean','Michael Jackson','19','https://www.youtube.com/watch?v=Zi_XLOBDo_Y','Via Filodrammatici, 2, 20121 Milano MI, Italia','17/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Demons','Imagine Dragons','20','https://www.youtube.com/watch?v=mWRsgZuwf_8','Corso Sebastopoli, 123, 10134 Torino TO, Italia','08/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Where Have You Been','Rihanna','21','https://www.youtube.com/watch?v=HBxt_v0WF6Y','Mercedes-Platz 1, 10243 Berlín, Alemania','04/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Wonderwall','Oasis','22','https://www.youtube.com/watch?v=6hzrDeceEKc','Willy-Brandt-Platz 3, 50679 Köln, Alemania','18/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Blank Space','Taylor Swift','23','https://www.youtube.com/watch?v=e-ORhEE9VVg','Olympiapark München, Spiridon-Louis-Ring 21, 80809 München, Alemania','01/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Sweet Child o Mine','Guns N Roses','24','https://www.youtube.com/watch?v=1w7OgIMMRc4','Sylvesterallee 7, 22525 Hamburg, Alemania','10/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Dont Stop Believin','Journey','25','https://www.youtube.com/watch?v=1k8craCGpgs','Messe Frankfurt Venue GmbH, Ludwig-Erhard-Anlage 1, 60327 Frankfurt am Main, Alemania','14/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Shape of You','Ed Sheeran','26','https://www.youtube.com/watch?v=JGwWNGJdvx8','4 Pennsylvania Plaza, Nueva York, NY 10001, Estados Unidos','15/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Sweet Caroline','Neil Diamond','27','https://www.youtube.com/watch?v=4F_RCWVoL4s','1 MetLife Stadium Dr, East Rutherford, NJ 07073, Estados Unidos','11/05/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Livin on a Prayer','Bon Jovi','28','https://www.youtube.com/watch?v=lDK9QqIzhwk','3900 W Manchester Blvd, Inglewood, CA 90305, Estados Unidos','21/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Stitches','Shawn Mendes','29','https://www.youtube.com/watch?v=VbfpW0pbvaU','1500 Sugar Bowl Dr, Nueva Orleans, LA 70112, Estados Unidos','07/06/2024');
INSERT INTO song (name, singer, id, url, concert_location, concert_date) VALUES ('Eye of the Tiger','Survivor','30','https://www.youtube.com/watch?v=btPJPFnesV4','STAPLES Center, 1111 S Figueroa St, Los Angeles, CA 90015, Estados Unidos','31/05/2024');


INSERT INTO playlist_songs (playlist_id, song_id) VALUES ('1', '1');
INSERT INTO playlist_songs (playlist_id, song_id) VALUES ('1', '2');
INSERT INTO playlist_songs (playlist_id, song_id) VALUES ('2', '3');
INSERT INTO playlist_songs (playlist_id, song_id) VALUES ('2', '4');
INSERT INTO playlist_songs (playlist_id, song_id) VALUES ('2', '5');

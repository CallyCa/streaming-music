from models.user import User
from models.auth import Auth
from models.song import Song
from models.playlist import Playlist
from extensions.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_test_user(name='John Doe', email='john@example.com', password='password123'):
    """
    Cria um usuário de teste no banco de dados.

    :param name: Nome do usuário
    :param email: Email do usuário
    :param password: Senha do usuário
    :return: Usuário criado
    """
    # Verificar e deletar qualquer usuário existente com o mesmo e-mail
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()

    auth = Auth(email=email, password=generate_password_hash(password), user_id=user.id)
    db.session.add(auth)
    db.session.commit()

    return user

def create_test_song(title='New Song', artist='John Doe', album='New Album', duration=240):
    """
    Cria uma música de teste no banco de dados.

    :param title: Título da música
    :param artist: Artista da música
    :param album: Álbum da música
    :param duration: Duração da música em segundos
    :return: Música criada
    """
    song = Song(title=title, artist=artist, album=album, duration=duration)
    db.session.add(song)
    db.session.commit()
    return song

def create_test_playlist(name='New Playlist', description='My favorite songs', user_id=None):
    """
    Cria uma playlist de teste no banco de dados.

    :param name: Nome da playlist
    :param description: Descrição da playlist
    :param user_id: ID do usuário dono da playlist
    :return: Playlist criada
    """
    playlist = Playlist(name=name, description=description, user_id=user_id)
    db.session.add(playlist)
    db.session.commit()
    return playlist

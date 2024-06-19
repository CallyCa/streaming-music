# locustfile.py
from faker import Faker
from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.faker = Faker("pt_BR")
        self.name = None
        self.email = None
        self.password = None

    def on_start(self):
        """Será executado quando o locust iniciar."""
        self.register()
        self.login()

    def register(self):
        """Registrar um novo usuário."""
        self.name = self.faker.name()
        self.email = self.faker.email()
        self.password = self.faker.password(length=12, special_chars=True, digits=True)
        response = self.client.post("/register", json={
            "name": self.name,
            "email": self.email,
            "password": self.password
        })
        if response.status_code == 201:
            print("Usuário registrado com sucesso!")
        else:
            print("Erro ao registrar o usuário.")

    def login(self):
        """Fazer login com o usuário registrado."""
        response = self.client.post("/login", json={
            "email": self.email,
            "password": self.password
        })
        if response.status_code == 200:
            token = response.json()["access_token"]
            self.client.headers.update({"Authorization": f"Bearer {token}"})
            print("Login realizado com sucesso!")
        else:
            print("Erro ao fazer login.")

    @task(1)
    def get_users(self):
        """Obter a lista de usuários."""
        self.client.get("/users")

    @task(2)
    def create_playlist(self):
        """Criar uma nova playlist."""
        self.client.post("/playlists", json={
            "name": self.faker.sentence(3)
        })

    @task(3)
    def get_playlists(self):
        """Obter a lista de playlists."""
        self.client.get("/playlists")

    @task(4)
    def create_song(self):
        """Criar uma nova música."""
        self.client.post("/songs", json={
            "title": self.faker.municipality(),
            "artist": self.faker.name_nonbinary(),
            "album": self.faker.sentence(3),
            "duration": self.faker.time_delta().total_seconds()
        })

    @task(5)
    def get_songs(self):
        """Obter a lista de músicas."""
        self.client.get("/songs")

    @task(6)
    def create_user(self):
        """Criar um novo usuário."""
        self.client.post("/users", json={
            "name": self.faker.name(),
            "email": self.faker.email(),
            "password": self.faker.password()
        })

    @task(7)
    def update_user(self):
        """Atualizar um usuário existente."""
        user_id = 1
        self.client.put(f"/users/{user_id}", json={
            "name": self.faker.name(),
            "email": self.faker.email(),
            "password": self.faker.password()
        })

    @task(8)
    def delete_user(self):
        """Excluir um usuário existente."""
        user_id = 1
        self.client.delete(f"/users/{user_id}")

    @task(9)
    def update_song(self):
        """Atualizar uma música existente."""
        song_id = 1
        self.client.put(f"/songs/{song_id}", json={
            "title": self.faker.sentence(4),
            "artist": self.faker.name_nonbinary(),
            "album": self.faker.street_name(),
            "duration": self.faker.time_delta().total_seconds()
        })

    @task(10)
    def delete_song(self):
        """Excluir uma música existente."""
        song_id = 1
        self.client.delete(f"/songs/{song_id}")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

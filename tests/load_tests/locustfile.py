# locustfile.py

from locust import HttpUser, TaskSet, task, between
import random
import string

class UserBehavior(TaskSet):

    def on_start(self):
        """Será executado quando o locust iniciar."""
        self.register()
        self.login()

    def random_string(self, length=10):
        """Gerar uma string aleatória de caracteres alfanuméricos."""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in length)

    def register(self):
        """Registrar um novo usuário."""
        self.email = f"{self.random_string()}@example.com"
        self.password = self.random_string()
        response = self.client.post("/register", json={
            "name": f"Locust Test {self.random_string()}",
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
            self.token = response.json()["access_token"]
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
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
            "name": f"Locust Playlist {self.random_string()}"
        })

    @task(3)
    def get_playlists(self):
        """Obter a lista de playlists."""
        self.client.get("/playlists")

    @task(4)
    def create_song(self):
        """Criar uma nova música."""
        self.client.post("/songs", json={
            "title": f"Locust Song {self.random_string()}",
            "artist": f"Locust Artist {self.random_string()}",
            "album": f"Locust Album {self.random_string()}",
            "duration": random.randint(200, 400)
        })

    @task(5)
    def get_songs(self):
        """Obter a lista de músicas."""
        self.client.get("/songs")

    @task(6)
    def create_user(self):
        """Criar um novo usuário."""
        email = f"{self.random_string()}@example.com"
        self.client.post("/users", json={
            "name": f"New Locust User {self.random_string()}",
            "email": email,
            "password": self.random_string()
        })

    @task(7)
    def update_user(self):
        """Atualizar um usuário existente."""
        user_id = 1
        self.client.put(f"/users/{user_id}", json={
            "name": f"Updated Locust User {self.random_string()}",
            "email": f"updatedlocust{self.random_string()}@example.com",
            "password": self.random_string()
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
            "title": f"Updated Locust Song {self.random_string()}",
            "artist": f"Updated Locust Artist {self.random_string()}",
            "album": f"Updated Locust Album {self.random_string()}",
            "duration": random.randint(200, 400)
        })

    @task(10)
    def delete_song(self):
        """Excluir uma música existente."""
        song_id = 1
        self.client.delete(f"/songs/{song_id}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

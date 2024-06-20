# locustfile.py
import logging
import os
import random

from faker import Faker
from locust import HttpUser, TaskSet, task, between

from tests.load_tests.locust_graphql import LocustGraphQL
from tests.load_tests.locust_rest import LocustREST


class UserBehavior(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logging.getLogger("locustfile")
        self.faker = Faker("pt_BR")
        self.name = None
        self.email = None
        self.password = None
        self.api_client = None
        api_type = os.getenv("API_TYPE")
        if api_type == "REST":
            self.api_client = LocustREST(self.client)
        elif api_type == "GraphQL":
            self.api_client = LocustGraphQL(self.client)

    def on_start(self):
        """Será executado quando o locust iniciar."""
        self.register()
        self.login()

    def register(self):
        """Registrar um novo usuário."""
        self.name = self.faker.name()
        self.email = self.faker.email()
        self.password = self.faker.password()
        response = self.api_client.register(self.name, self.email, self.password)
        if response.status_code == 200 or response.status_code == 201:
            self.logger.info("Usuário registrado com sucesso!")
        else:
            self.logger.info("Erro ao registrar o usuário.")

    def login(self):
        """Fazer login com o usuário registrado."""
        response = self.api_client.login(self.email, self.password)
        if response.status_code == 200:
            if "access_token" in response.json():
                token = response.json()["access_token"]
            elif "data" in response.json():
                token = response.json()["data"]["loginUser"]["accessToken"]
            else:
                token = None
            self.client.headers.update({"Authorization": f"Bearer {token}"})
            self.logger.info("Login realizado com sucesso!")
        else:
            self.logger.info("Erro ao fazer login.")

    @task(1)
    def get_users(self):
        """Obter a lista de usuários."""
        self.api_client.get_users()

    @task(3)
    def create_playlist(self):
        """Criar uma nova playlist."""
        self.api_client.create_playlist(self.faker.sentence(3))

    @task(4)
    def get_playlists(self):
        """Obter a lista de playlists."""
        self.api_client.get_playlists()

    @task(5)
    def create_song(self):
        """Criar uma nova música."""
        self.api_client.create_song(
            title=self.faker.sentence(),
            artist=self.faker.name_nonbinary(),
            album=self.faker.sentence(3),
            duration=self.faker.time_delta().total_seconds()
        )

    @task(5)
    def get_songs(self):
        """Obter a lista de músicas."""
        self.api_client.get_songs()

    @task(2)
    def create_user(self):
        """Criar um novo usuário."""
        self.api_client.create_user(
            name=self.faker.name(),
            email=self.faker.email(),
            password=self.faker.password()
        )

    @task(1)
    def update_user(self):
        """Atualizar um usuário existente."""
        users = self.api_client.get_users().json()
        if users is list:
            user_id = random.choice(users)["id"]
        elif "data" in users:
            user_id = random.choice(users["data"]["allUsers"])["id"]
        else:
            user_id = 0
        self.api_client.update_user(
            user_id,
            name=self.faker.name(),
            email=self.faker.email(),
            password=self.faker.password()
        )

    @task(1)
    def delete_user(self):
        """Excluir um usuário existente."""
        users = self.api_client.get_users().json()
        if users is list:
            user_id = random.choice(users)["id"]
        elif "data" in users:
            user_id = random.choice(users["data"]["allUsers"])["id"]
        else:
            user_id = 0
        self.api_client.delete_user(user_id)

    @task(1)
    def update_song(self):
        """Atualizar uma música existente."""
        songs = self.api_client.get_songs().json()
        if songs is list:
            song_id = random.choice(songs)["id"]
        elif "data" in songs:
            song_id = random.choice(songs["data"]["allSongs"])["id"]
        else:
            song_id = 0
        self.api_client.update_song(
            song_id,
            title=self.faker.sentence(4),
            artist=self.faker.name_nonbinary(),
            album=self.faker.street_name(),
            duration=self.faker.time_delta().total_seconds()
        )

    @task(1)
    def delete_song(self):
        """Excluir uma música existente."""
        songs = self.api_client.get_songs().json()
        if songs is list:
            song_id = random.choice(songs)["id"]
        elif "data" in songs:
            song_id = random.choice(songs["data"]["allSongs"])["id"]
        else:
            song_id = 0
        self.api_client.delete_song(song_id)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 1)

from tests.load_tests.locust_api import LocustAPI


class LocustREST(LocustAPI):
    """Cliente REST para o Locust"""

    def register(self, name, email, password):
        return self.client.post("/register", json={
            "name": name,
            "email": email,
            "password": password
        })

    def login(self, email, password):
        return self.client.post("/login", json={
            "email": email,
            "password": password
        })

    def create_user(self, name, email, password):
        return self.client.post("/users", json={
            "name": name,
            "email": email,
            "password": password
        })

    def update_user(self, user_id, name, email, password):
        return self.client.put(f"/users/{user_id}", json={
            "name": name,
            "email": email,
            "password": password
        })

    def delete_user(self, user_id):
        return self.client.delete(f"/users/{user_id}")

    def get_users(self):
        return self.client.get("/users")

    def create_song(self, title, artist, album, duration):
        return self.client.post("/songs", json={
            "title": title,
            "artist": artist,
            "album": album,
            "duration": duration
        })

    def update_song(self, song_id, title, artist, album, duration):
        return self.client.put(f"/songs/{song_id}", json={
            "title": title,
            "artist": artist,
            "album": album,
            "duration": duration
        })

    def delete_song(self, song_id):
        return self.client.delete(f"/songs/{song_id}")

    def get_songs(self):
        return self.client.get("/songs")

    def create_playlist(self, name):
        return self.client.post("/playlists", json={
            "name": name
        })

    def get_playlists(self):
        return self.client.get("/playlists")

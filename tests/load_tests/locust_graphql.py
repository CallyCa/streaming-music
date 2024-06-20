from typing import List

from tests.load_tests.locust_api import LocustAPI


class LocustGraphQL(LocustAPI):
    """Cliente GraphQL para o Locust"""

    def register(self, name, email, password):
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($input: UserInput!) {
                    registerUser(input: $input) {
                        user { id }
                    }
                }
            ''',
            "variables": {
                "input": {
                    "name": name,
                    "email": email,
                    "password": password
                }
            }
        })

    def login(self, email, password):
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($input: AuthInput!) {
                    loginUser(input: $input) {
                        accessToken
                    }
                }
            ''',
            "variables": {
                "input": {
                    "email": email,
                    "password": password
                }
            }
        })

    def create_user(self, name, email, password):
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($name: String, $email: String, $password: String) {
                    createUser(input: {
                        "name": $name,
                        "email": $email,
                        "password": $password
                    }) { id }
                }
            ''',
            "variables": {
                "name": name,
                "email": email,
                "password": password
            }
        })

    def update_user(self, user_id, name, email, password):
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($input: UserInput!) {
                    updateUser(input: $input) {
                        user { id }
                    }
                }
            ''',
            "variables": {
                "input": {
                    "name": name,
                    "email": email,
                    "password": password
                }
            }
        })

    def delete_user(self, user_id):
        return self.client.post("/graphql", json={
            "query": '''
                mutation {
                    deleteUser(id: $id) {
                        ok
                    }
                }
                ''',
            "variables": {
                "id": user_id
            }
        })

    def get_users(self):
        return self.client.post("/graphql", json={
            "query": '''
                query {
                    allUsers {
                        id,
                        name,
                        email
                    }
                }
            '''
        })

    def create_song(self, title, artist, album, duration):
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($input: SongInput!) {
                    createSong(input: $input) {
                        song {
                            id
                        }
                    }
                }
                ''',
            "variables": {
                "input": {
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "duration": duration
                }
            }
        })

    def update_song(self, song_id, title, artist, album, duration):
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($input: SongInput!) {
                    updateSong(input: $input) {
                        song {
                            id
                        }
                    }
                }
            ''',
            "variables": {
                "input": {
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "duration": duration
                }
            }
        })

    def delete_song(self, song_id):
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($input: SongInput!) {
                    deleteSong(id: $id) {
                        ok
                    }
                }
            ''',
            "variables": {
                "id": song_id
            }
        })

    def get_songs(self):
        return self.client.post("/graphql", json={
            "query": '''
                query {
                    allSongs {
                        id,
                        title,
                        artist,
                        album,
                        duration
                    }
                }
            '''
        })

    def create_playlist(self, name, songs=None):
        if songs is None:
            songs = []
        return self.client.post("/graphql", json={
            "query": '''
                mutation ($input: SongInput!) {
                    createPlaylist(input: $input) {
                        playlist {
                            id
                        }
                    }
                }
            ''',
            "variables": {
                "input": {
                    "name": name,
                    "songs": songs
                }
            }
        })

    def get_playlists(self):
        return self.client.post("/graphql", json={
            "query": '''
            query {
                allPlaylists {
                    id,
                    name,
                    userId,
                    songs {
                        id
                    }
                }
            }
            '''
        })

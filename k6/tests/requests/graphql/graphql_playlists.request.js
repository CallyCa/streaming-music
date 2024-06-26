import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';

const url = env.URL_TEST.SERVREST;

export default class GraphQLPlaylists {
    constructor() {
        this.params = {
            headers: {
                'Content-Type': 'application/json',
                monitor: false,
            },
        };
    }

    list(token) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                query {
                    allPlaylists {
                        id
                        name
                        user_id
                        songs {
                            id
                            title
                            artist
                            album
                            duration
                        }
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });

        return response.json('data.allPlaylists');
    }

    create(token, name) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    createPlaylist(input: { name: "${name}" }) {
                        playlist {
                            id
                            name
                        }
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });

        return response.json('data.createPlaylist.playlist');
    }

    update(token, id, data) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    updatePlaylist(id: ${id}, input: { name: "${data.name}" }) {
                        playlist {
                            id
                            name
                        }
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }

    delete(token, id) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    deletePlaylist(id: ${id}) {
                        success
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }

    getBySongId(token, song_id) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                query {
                    playlistsBySong(song_id: ${song_id}) {
                        id
                        name
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });

        return response.json('data.playlistsBySong');
    }

    removeSong(token, playlist_id, song_id) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    removeSongFromPlaylist(playlist_id: ${playlist_id}, song_id: ${song_id}) {
                        playlist {
                            id
                            name
                        }
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }
}

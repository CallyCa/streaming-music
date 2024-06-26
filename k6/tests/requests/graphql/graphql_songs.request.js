import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';

const url = env.URL_TEST.SERVREST;

export default class GraphQLSongs {
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
                    allSongs {
                        id
                        title
                        artist
                        album
                        duration
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });

        return response.json('data.allSongs');
    }

    create(token, title, artist, album, duration) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    createSong(input: { title: "${title}", artist: "${artist}", album: "${album}", duration: ${duration} }) {
                        song {
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

        return response.json('data.createSong.song');
    }

    update(token, id, data) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    updateSong(id: ${id}, input: { title: "${data.title}", artist: "${data.artist}", album: "${data.album}", duration: ${data.duration} }) {
                        song {
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
    }

    delete(token, id) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    deleteSong(id: ${id}) {
                        ok
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

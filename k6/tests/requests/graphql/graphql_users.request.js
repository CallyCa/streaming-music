import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';
import { faker } from '@faker-js/faker';

const url = env.URL_TEST.SERVREST;

export default class GraphQLUsers {
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
                    allUsers {
                        id
                        name
                        email
                        nickname
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }

    create(token, nickname) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    createUser(input: {nickname: "${nickname}"}) {
                        user {
                            id
                            name
                            email
                            nickname
                        }
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
        });

        return response.json('data.createUser.user');
    }

    update(token, id, data) {
        this.params.headers['Authorization'] = `Bearer ${token}`;
        let payload = JSON.stringify({
            query: `
                mutation {
                    updateUser(id: ${id}, input: { name: "${data.name}", email: "${data.email}", nickname: "${data.nickname}" }) {
                        user {
                            id
                            name
                            email
                            nickname
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
                    deleteUser(id: ${id}) {
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
}

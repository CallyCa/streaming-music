import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';

const url = env.URL_TEST.SERVREST;

export default class GraphQLLogin {
    constructor() {
        this.params = {
            headers: {
                'Content-Type': 'application/json',
                monitor: false,
            },
        };
        this.token = '';
    }

    access(email, password) {
        let payload = JSON.stringify({
            query: `
                mutation {
                    loginUser(input: {email: "${email}", password: "${password}"}) {
                        accessToken
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        check(response, {
            'is status 200': () => response.status === 200,
            'Token generated': (r) => r.json('data.loginUser.accessToken') !== null,
        });

        if (response.json('data.loginUser.accessToken')) {
            this.token = response.json('data.loginUser.accessToken');
        } else {
            console.error('Login failed:', response.body);
        }
    }

    getToken() {
        return this.token;
    }
}

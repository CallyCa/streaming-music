import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';

const url = env.URL_TEST.SERVREST;

export default class Login {
    constructor() {
        this.params = {
            headers: {
                accept: 'application/json',
                'Content-Type': 'application/json',
                monitor: false,
            },
        };
        this.token = '';
    }

    access(email, password) {
        let payload = JSON.stringify({
            email: email,
            password: password,
        });

        let response = http.post(`${url}/login`, payload, this.params);
        this.token = response.json('access_token');
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }

    getToken() {
        return this.token;
    }
}

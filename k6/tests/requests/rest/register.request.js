import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';

const url = env.URL_TEST.SERVREST;

export default class Register {
    constructor() {
        this.params = {
            headers: {
                accept: 'application/json',
                'Content-Type': 'application/json',
                monitor: false,
            },
        };
    }

    generateRandomEmail() {
        return `user_${Math.random().toString(36).substring(2, 15)}@example.com`;
    }

    create() {
        const email = this.generateRandomEmail();
        const payload = JSON.stringify({
            email: email,
            name: "Random User",
            password: "testpassword",
        });

        const response = http.post(`${url}/register`, payload, this.params);
        check(response, {
            'is status 201': () => response.status === 201,
        });

        return { email: email, password: "testpassword" };
    }
}

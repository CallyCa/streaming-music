import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';

const url = env.URL_TEST.SERVREST;

export default class Users {
    constructor() {
        this.params = {
            headers: {
                accept: 'application/json',
                'Content-Type': 'application/json',
                monitor: false,
            },
        };
    }

    list(token) {
        let response = http.get(`${url}/users`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                accept: 'application/json',
                'Content-Type': 'application/json',
                monitor: false,
            },
        });
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }

    create(token, nickname) {
        const payload = JSON.stringify({
            nickname: nickname,
        });

        let response = http.post(`${url}/users`, payload, {
            headers: {
                'Authorization': `Bearer ${token}`,
                accept: 'application/json',
                'Content-Type': 'application/json',
                monitor: false,
            },
        });
        check(response, {
            'is status 201': () => response.status === 201,
        });

        return response.json();
    }

    update(token, id, data) {
        let response = http.put(`${url}/users/${id}`, JSON.stringify(data), {
            headers: {
                'Authorization': `Bearer ${token}`,
                accept: 'application/json',
                'Content-Type': 'application/json',
                monitor: false,
            },
        });
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }

    delete(token, id) {
        let response = http.del(`${url}/users/${id}`, null, {
            headers: {
                'Authorization': `Bearer ${token}`,
                accept: 'application/json',
                'Content-Type': 'application/json',
                monitor: false,
            },
        });
        check(response, {
            'is status 200': () => response.status === 200,
        });
    }
}

import { check } from 'k6';
import http from 'k6/http';
import env from '../../services/api/routes/index.js';
import { faker } from '@faker-js/faker';

const url = env.URL_TEST.SERVREST;

export default class GraphQLRegister {
    constructor() {
        this.params = {
            headers: {
                'Content-Type': 'application/json',
                monitor: false,
            },
        };
    }

    create() {
        const email = faker.internet.email();
        const password = faker.internet.password();
        const name = faker.person.fullName();

        let payload = JSON.stringify({
            query: `
                mutation {
                    registerUser(input: {name: "${name}", email: "${email}", password: "${password}"}) {
                        user {
                            id
                            name
                            email
                        }
                    }
                }
            `,
        });

        let response = http.post(`${url}/graphql`, payload, this.params);
        const isStatus200 = response.status === 200;
        const userCreated = response.json('data.registerUser.user') !== null;

        check(response, {
            'is status 200': () => isStatus200,
            'User created': () => userCreated,
        });

        if (isStatus200 && userCreated) {
            return {
                email: email,
                password: password,
                user: response.json('data.registerUser.user')
            };
        } else {
            console.error('User creation failed:', response.json());
            return null;
        }
    }
}

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

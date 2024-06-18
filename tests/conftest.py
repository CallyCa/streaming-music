import pytest
from app import create_app
from extensions.extensions import db

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Cria um contexto de aplicação
    with flask_app.app_context():
        # Cria todas as tabelas
        db.create_all()

        yield flask_app.test_client()  # Testa aqui

        # Remove todas as tabelas
        db.drop_all()
